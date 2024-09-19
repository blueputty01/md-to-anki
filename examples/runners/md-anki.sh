#!/bin/bash

# Change the directory to D:
cd /Users/alexyang/Documents/School/anki/md-to-anki/src || exit

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python main.py

# Deactivate the virtual environment (optional)
deactivate