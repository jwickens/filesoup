.. Filesoup's documentation master file

Welcome to Filesoup's documentation!
=======================================
This is a small webapp I wrote for a recruiter to demonstrate my programming abilities. The challange was described as the following:
	
	Using Python, Celery, Flask, and SQLite - could you please create a small web application,
	which will scan the local folders and get information about the files, size, age, etc.
	Can you then save it to the database and create 2 API endpoints:
        - list of all files
        - information about single file.
	result should be displayed in JSON format
	Folder scanning should be deployed as a background task in Celery. Please upload to GitHub and send us repository URL to review.


I decided to use a virtualenv to ensure dependencies are followed. These dependencies are listed in :doc:`requirements`


The application can be started with the following command from the shell::
        ./run.py

Please see :doc:`running` for more information on how to run the app.

Contents
========
.. toctree::
   :maxdepth: 1

   api
   requirements
   running



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Reflections
===========
Stephen wanted me to provide a cover letter with some reflections on this project, which I will do here. Development of this application went rather smoothly, and I 
found Flask very familiar because of my experience with Django. Django's ORM is also very similiar to SQLAlchemy. Celery, however, was a new challenge as I've never 
approached distributed computing. I had to think for a long while about how to use it correctly, and decided that the local client will have to do the majority of the 
work in terms of file watching. Celery comes in by grabbing up very short tasks to write to the database. I had to refactor my code quite a bit to have a satisfactory 
testing environment, and I ended up creating a lot of factories. These paid off however, as I don't think I could have gotten Celery to work well at all with out 
unittest.
