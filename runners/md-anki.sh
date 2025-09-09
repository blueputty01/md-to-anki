#!/bin/zsh

# Change the directory to D:
cd /Users/alexyang/Documents/anki/md-to-anki || exit

# Activate the virtual environment
source venv/bin/activate

cd src || exit

# Run the Python script
python main.py "$@" # pass all arguments to the script

# Deactivate the virtual environment (optional)
deactivate
