"""Copies the requirements list used by pip into the sphinx entry for requirements/dependencies."""
import os
wd = os.path.dirname(os.path.abspath(__file__))
parent = os.path.split(wd)[0]
with open(os.path.join(parent, 'requirements.txt', 'r')) as requirements_pip:
	with open(os.path.join(wd, 'requirements.rst','w') as requirements_sphinx:
		requirements_sphinx.write('.. _requirements:\n\n')
		requirements_sphinx.write('Requirements\n')
		requirements_sphinx.write('============\n\n')
		for line in requirements_pip:
			requirements_sphinx.write('* ' + line)

