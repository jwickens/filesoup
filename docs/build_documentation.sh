#!/bin/sh
echo 'Building documentation...\n================='
cd ..
export PYTHONPATH=$(pwd)
export PYTHONPATH=$PYTHONPATH:$(pwd)/app
cd docs
python copy_requirements.py
make html
