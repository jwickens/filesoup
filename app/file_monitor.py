import time, logging, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.tasks import delete_file, create_file, update_file
from app.setup.config import EXAMPLE_FILES_LOCATION

class UpdateDatabaseHandler(FileSystemEventHandler):
	"""Starts celery tasks to update the database on file events."""

	def __init__(self, testing=False):
		self._testing = testing
		super(UpdateDatabaseHandler, self).__init__()
	
	def on_moved(self, event):
		"""Triggered when a file is moved, which now must be deleted from the Database"""
		self._delete(event)

	def on_created(self, event):
		"""Triggered when a new file is created, which now must be recorded to the Database"""
		self._record(event)
	
	def on_deleted(self, event):
		"""Triggered when a file is deleted, which now must be deleted from the Database"""
		self._delete(event)

	def on_modified(self, event):
		"""Triggered when a file is modified, which now must be modified in the Database"""
		self._update(event)

	def _delete(self, event):
		"""Starts a celery task to delete the file from the database."""
		self._wait(delete_file, [event.src_path])

	def _record(self, event):
		"""Starts a celery task to add the file to the database."""
		self._wait(create_file, [event.src_path, os.stat(event.src_path)])


	def _update(self, event):
		"""Starts a celery task to update the file from the database."""
		self._wait(update_file, [event.src_path, os.stat(event.src_path)])

	def _wait(self, task, args):
		"""A wrapper to use celery's apply_async."""
		if not self._testing:
			task.apply_async(args, priority=0)
		else:
			print task, args

def schedule_observer(path=EXAMPLE_FILES_LOCATION, testing=False):
	"""Creates an file directory observer and schedules it to use the UpdateDabaseHandler that in turn calls the Celery tasks."""
	event_handler = UpdateDatabaseHandler(testing)
	observer = Observer()
	observer.schedule(event_handler, path=path, recursive=False)
	return observer

if __name__ == "__main__":
	observer = schedule_observer()
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
