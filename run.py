#!bin/python
"""Starts a flask app, loads initial directory info into the database, and starts a watchdog observer that will kick-off celery tasks in response to directoy 
events."""
import os, time
from celery import states, Celery
from celery.exceptions import TimeoutError
from app.setup.database import get_engine, get_session_from_engine, create_base, initialize_base
from app.setup.config import DATABASE_CONFIG, FLASK_CONFIG
from app.setup.create_flask import create_flask
from app.tasks import celery, create_file, update_file, delete_file, discover_files, verify_files
from app.file_monitor import schedule_observer
from app.models import Archive, Base
from multiprocessing import Process

#DATABASE
db_engine = get_engine(DATABASE_CONFIG.URI)
db = get_session_from_engine(db_engine)
create_base(Base, db_engine)
if not os.path.exists(DATABASE_CONFIG.LOCATION):
	initialize_base(db)

#INITIAL DIRECTORY DATA
def hard_check_files():
	try:
		discover_files(immediate=db)
		verify_files().apply_async(timeout=10)
	except TimeoutError:
		pass
hard_check_files()


#FLASK
flask_app = create_flask(FLASK_CONFIG, DATABASE_CONFIG)
def run_server():
    flask_app.run()
server = Process(target=run_server)


#START
obs = schedule_observer()
obs.start()
server.start()

try:
	while True:
		time.sleep(60*60)
		hard_check_files()
except KeyboardInterrupt:
		obs.stop()
		server.terminate()
obs.join()
server.join()
