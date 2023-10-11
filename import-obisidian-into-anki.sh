#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Import Obisidian into Anki
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Anki Utils

# Documentation:
# @raycast.description Imports markdown files into Anki
# @raycast.author Alexander Yang
# @raycast.authorURL github.com/blueputty01

# Change the directory to D:
cd /Users/alexyang/Documents/School/anki/md-to-anki/

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python main.py

# Deactivate the virtual environment (optional)
deactivate