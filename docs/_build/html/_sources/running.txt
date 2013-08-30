.. _running:

==================
How to run the app
==================

Getting the various dependencies to work with each other was the hardest part of this challenge. Because I hope that these complications do not get in the way of the 
code review, I'll try my best here to provide some hints.

Celery
________
Celery in particular needs a lot of babysitting to get running.
1. Celery must be run with the application option, -A app.tasks for normal runtime. See the scripts in utils for more information on how I ran Celery.
2. The application is set up to use RabbitMQ as both a backend and a broker. Please ensure RabbitMQ is running before starting Celery.


SQLite
______
Since the database is SQLite, it is easy to administer it. For purposes of the Demo, db files can always be deleted and run.py or tests.py or will re-create them.

Creating Files
________________
utils/create_random_files.sh is a bash script to create random files in the example_files directory. While it might be good for heavy load testing, my app isn't quite 
ready for thousands of files. I suggest moving files in and out, editing them, and deleting them within the example_files directory.

Testing 
______________
To make sure imports work be sure to run python like this (from the project dir):
        python -m app.utils.celery_tests

The initial file discovery function, discover_files, fails in the test where the database writes are propogated across celery. This may be because the group takes too 
long to return, as the error states. I tried my best to fix this but it didn't seem as important as other things.

Running
________

Finally! In the project directory the run.py script can be run. Flask's development server should start up and you can go to the web to test /files!
