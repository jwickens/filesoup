"""
Defines the tasks that update the database with new files. Some tasks are meant to be run locally and are not celery tasks.
"""
from os.path import join, split
from os import stat, walk
from celery.signals import task_postrun
from celery import Task, Celery, group
from app.models import Archive
from app.setup.database import get_session_from_uri
from app.setup.config import DATABASE_CONFIG, DATABASE_TESTING_CONFIG, CELERY_CONFIG, EXAMPLE_FILES_LOCATION

celery = Celery(__name__)
celery.config_from_object(CELERY_CONFIG)

class DatabaseTask(Task):
	"""Ensures that tasks connect and disconnect to the database."""
	abstract = True
	_db_session = None

	def __call__(self, *args, **kwargs):
		if 'testing' in kwargs:
			self.testing = kwargs['testing']
			del kwargs['testing']
		else:
			self.testing = False
		self.run(*args, **kwargs)

	def file_name(self, location):
		"""Extracts the file name out of the location"""
		return split(location)[1]

	def mapping(self, location, stat):
		"""Provides a dictionary to easily extract information from location and stat that is relevent to the Archive model."""
		return {
				'file_name': self.file_name(location),
				'size': stat.st_size,
				'modified': stat.st_mtime,
				'created': stat.st_ctime,
			}

	@property
	def db_session(self):
		if self._db_session is None:
			if self.testing:
				self._db_session = get_session_from_uri(DATABASE_TESTING_CONFIG.URI)
			else:
				self._db_session = get_session_from_uri(DATABASE_CONFIG.URI)
		return self._db_session

	def on_success(self, *args, **kwargs):
		self.db_session.commit()

	def after_return(self, *args, **kwargs):
		if self._db_session:
			self._db_session.remove()

@celery.task(base=DatabaseTask, name='app.tasks.update_file')
def update_file(location, stat):
	"""Updates the database archive with information from an os.stat object."""
	self = update_file #using bind=True to make self available raises a "TypeError: 'bool' object is not callable"
	archive = self.db_session.query(Archive).filter_by(file_name=self.file_name(location))
	archive.update(self.mapping(location,stat))

@celery.task(base=DatabaseTask, name='app.tasks.create_file')
def create_file(location, stat):
	"""Creates a new archive entry with information from an os.stat object."""
	self = create_file
	archive = Archive(**self.mapping(location, stat))
	self.db_session.add(archive)

@celery.task(base=DatabaseTask, name='app.tasks.delete_file')
def delete_file(location):
	self=delete_file
	"""Deletes an archive entry."""
	archive = self.db_session.query(Archive).filter_by(file_name=self.file_name(location)).first()
	self.db_session.delete(archive)


def discover_files(location = EXAMPLE_FILES_LOCATION, testing=False, immediate=False):
	"""Walks through a given location to disover all unknown files. If immediate is not False it must provide a db_session object."""
	results = []
	for root, dirs, files in walk(location):
		for archive in files:
			result = Archive.query.filter_by(file_name = archive).first()
			if not result:
				path = join(root, archive)
				st = stat(path)
				args = [path, st]
				kargs = {'testing': testing}
				if not immediate:
					results.append(create_file.subtask(args, kargs, priority=0))
				else:
					archive = Archive(**DatabaseTask().mapping(*args))
					immediate.add(archive)
					immediate.commit()
	if not immediate:
		return group(results)
	else:
		return None



def verify_file(file_obj, location = EXAMPLE_FILES_LOCATION, testing=False):
	"""Checks to see if a given file still exists and still has the same attributes. Syncronizes any changes."""
	path = join(location, file_obj.file_name)
	try:
		st = stat(path)
		if st.st_size != file_obj.size or st.st_mtime != file_obj.modified or st.st_ctime != file_obj.created:
			args = [path, st]
			return update_file.subtask(args, priority=0)
	except OSError:
		args = [path]
		kargs = {'testing': testing}
		return delete_file.subtask(args, kargs, priority=0)
	return None


def verify_files(location = EXAMPLE_FILES_LOCATION, testing=False):
	"""Goes through the files table and starts the verify_file task for each file record."""
	results = []
	for archive in Archive.query.all():
		res = verify_file(archive, location, testing)
		if res is not None:
			results.append(res)
	return group(results)
