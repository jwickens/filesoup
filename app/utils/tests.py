#!bin/python
"""Defines unittests for flask components of the app."""
import unittest, os, json, time
from celery import states, Celery
from celery.exceptions import TimeoutError
from app.setup.database import get_engine, get_session_from_engine, create_base
from app.setup.config import DATABASE_TESTING_CONFIG, CELERY_CONFIG, EXAMPLE_FILES_LOCATION, FLASK_TESTING_CONFIG
from app.setup.create_flask import create_flask
from app.tasks import celery, create_file, update_file, delete_file, discover_files, verify_files
from app.file_monitor import schedule_observer
from app.models import Archive, Base
FILES = {
		'file1': {
			'file_name': 'file1',
			'size': 500,
			'created': 1990326,
			'modified': 201366,
			},
		}


class TestCase(unittest.TestCase):
	def setUp(self):
		flask_app = create_flask(FLASK_TESTING_CONFIG, DATABASE_TESTING_CONFIG)
		self.flask_app = flask_app.test_client()
		self.db_engine = get_engine(DATABASE_TESTING_CONFIG.URI)
		self.db = get_session_from_engine(self.db_engine)
		create_base(Base, self.db_engine)

	def tearDown(self):
		self.db.remove()
		Base.metadata.drop_all(bind=self.db_engine)

	def write_file(self):
		"""Helper that writes an example file to the data base"""
		test_file = Archive(**FILES['file1'])
		self.db.add(test_file)
		self.db.commit()

	def check_content_type(self, response):
		"""Helper that checks for JSON"""
		assert response.headers['content-Type'] == 'application/json'

	def check_ok(self, response):
		"""Helper that checks to see if the HTTP response is 200"""
		assert response.status_code == 200

	def wait_on_task(self, task, args=None, kwargs=None):
		"""Helper for testing celery tasks"""
		def go():
			return task.apply_async(args, kwargs, priority=0)
		res = go()
		count = 0
		print res
		while res.successful() != True and count < 15:
			try:
				res.get(timeout=2)
			except TimeoutError as error:
				time.sleep(5)
				res = go()
				count += 1
		assert res.successful() == True



	def test_write_file(self):
		"""Tests if the Archive Model works for writing an example file to the database."""
		self.write_file()
		assert Archive.query.filter_by(file_name = 'file1').first() != None

	def test_read_files(self):
		"""Tests if we get the files data back in the form we want."""
		self.write_file()
		result = self.flask_app.get('files')
		self.check_content_type(result)
		self.check_ok(result)
		data = json.loads(result.data)
		assert set([u'file_name',u'size', u'created',u'modified']) == set(data['file1'].keys())

	def test_read_file(self):
		"""Tests if we get the JSON data for a single file in the form we want."""
		self.write_file()
		result = self.flask_app.get('files/file1')
		self.check_content_type(result)
		self.check_ok(result)
		data = json.loads(result.data)
		assert set([u'file_name',u'size', u'created',u'modified']) == set(data.keys())

	def test_discover_files(self):
		"""Tests if the celery task finds files"""
		g = discover_files(testing=True)
		self.wait_on_task(g)
		assert Archive.query.count() > 2

	def test_discover_files_sync(self):
		"""Tests if the celery task finds files, no celery functionality"""
		g = discover_files(testing=True, immediate=self.db)
		assert Archive.query.count() > 2

	def test_verify_files(self):
		"""Tests if the celery task syncronizes files... it should delete our example file; no actual celery functionality"""
		self.write_file()
		g = verify_files(testing=True)
		self.wait_on_task(g)
		assert Archive.query.filter_by(file_name = 'file1').first() == None

	def test_create_file(self):
		"""Checks the celery task create_file, full functionality (requires that celery is running)"""
		stat = os.stat('/')
		location = os.path.join(os.path.dirname(__file__), 'test')
		self.wait_on_task(create_file, [location, stat], {'testing':True})

	def test_update_file(self):
		"""Checks the celery task update_file, full functionality (requires that celery is running)"""
		archive = Archive(file_name='test')
		self.db.add(archive)
		self.db.commit()
		location = os.path.join(os.path.dirname(__file__), 'test')
		stat = os.stat('/')
		self.wait_on_task(update_file, [location, stat], {'testing':True})

	def test_delete_file(self):
		"""Checks the celery task delete_file, full functionality (requires that celery is running)"""
		archive = Archive(file_name='test')
		location = os.path.join(os.path.dirname(__file__), 'test')
		self.db.add(archive)
		self.db.commit()
		self.wait_on_task(delete_file, [location], {'testing':True})

	def test_file_monitor(self):
		"""Tests the file monitor by printing on screen the tasks that would be created. ToDo: automatically verify this output."""
		obs = schedule_observer(testing=True)
		obs.start()
		try:
			new_file_loc =os.path.join(EXAMPLE_FILES_LOCATION, 'test')
			#create
			with open(new_file_loc, 'w') as new_file:
				pass
			time.sleep(1)
			#modify
			with open(new_file_loc, 'w') as new_file:
				new_file.write('Hello!!!!!!!!!!!!!!')
			time.sleep(1)
			#delete, create
			ch_file_loc = os.path.join(EXAMPLE_FILES_LOCATION, 'still_test')
			os.rename(new_file_loc, ch_file_loc)
			time.sleep(1)
			#delete
			os.remove(ch_file_loc)
			time.sleep(1)
		except KeyboardInterrupt:
			pass
		finally:
			obs.stop()
			obs.join()


if __name__ == '__main__':
	unittest.main()
