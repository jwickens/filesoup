.. _api:


.. contents::
        :local:

=============
API Reference
=============

HTTP API
=========
These are the web hooks:

.. http:get:: /files/

        Lists all the files in JSON format.


.. http:get:: /files/<str:file_id>/

        Provides the date created, date modified, and size of the file whose name is equal to `file_id`.


Source Code Reference
=======================        

file_monitor
_____________
Implementation of watchdog, which allows cross-platform monitoring of files.

.. automodule:: app.file_monitor
        :members:

tasks
______
Methods to update the database in response to changes to the directory.

.. automodule:: app.tasks
        :members:

models
_______
Defines the Archive model which defines how I store file objects.

.. automodule:: app.models
        :members:

resources
__________
Defines the HTTP resources :http:get:`/files/` and :http:get:`/files/<str:file_id>/`.  

.. automodule:: app.resources
        :members:

views
_________
This module is more of a place keeper than anything.

.. automodule:: app.views
        :members:

setup.config
_____________
This is made to be at once flexible yet extendable. 

.. automodule:: app.setup.config
        :members:

setup.create_flask
__________________
The flask factory. Allows flexibility to define a different config objects, which is important for testing.

.. automodule:: app.setup.create_flask
        :members:

setup.database
_______________
Defines helper functions to create database sessions and bind them to mappings.

.. automodule:: app.setup.database
        :members:

utils.tests
___________
This module contains all application tests.

.. automodule:: app.utils.tests
        :members:

utils
______
Other scripts in this module help set up the app's environment. For instance, "create_random_files.sh" will create lots of random files in the app/example_files 
folder.
