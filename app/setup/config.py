"""Configuration settings for all application components"""
from os.path import abspath, join, split, dirname

SETUP_DIR = dirname(__file__)
APP_DIR = abspath(split(SETUP_DIR)[0]) #The app folder, above setup
EXAMPLE_FILES_LOCATION = join(APP_DIR, 'example_files')

class DatabaseConfig(object):
	"""Provides standardized Database configuration object"""
	LOCATION = None	 # The full path to the location of the database. Constructed on init by providing the database_file name.
	URI = None 	# The SQLite URI, also contructed on init.
	def __init__(self, database_file='app.db'):
		self.LOCATION = join(APP_DIR, database_file)
		self.URI = 'sqlite:///' + self.LOCATION
		
class CeleryConfig(object):
	"""Global Celery configurations, to be subclassed for further refinements."""
	BROKER_URL = 'amqp://guest@localhost//'
	CELERY_IMPORTS = ("app.tasks")
	CELERY_RESULT_BACKEND = "amqp"
	CELERY_DISABLE_RATE_LIMITS = True

class FlaskConfig(object):
	"""Development flask configuration"""
	DEBUG = True

class FlaskTestingConfig(FlaskConfig):
	"""Testing flask configuration"""
	TESTING = True

DATABASE_CONFIG = DatabaseConfig()
DATABASE_TESTING_CONFIG = DatabaseConfig('utils/test.db')
FLASK_CONFIG = FlaskConfig()
FLASK_TESTING_CONFIG = FlaskTestingConfig()
CELERY_CONFIG = CeleryConfig()
