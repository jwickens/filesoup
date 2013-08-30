"""Randomly changes the modify and access dates of files in the 'example_files' directory"""
import os
from random import randint
from datetime import datetime, timedelta

def random_date():
	start = datetime(1990,1,1)
	end = datetime(2012,12,31)
	dt = start + timedelta(seconds=randint(0, int((end - start).total_seconds())))
	return (dt - datetime(1970,1,1)).total_seconds()

for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'example_files')):
	for file in files:
		os.utime(os.path.join(root,file), (random_date(), random_date()))
