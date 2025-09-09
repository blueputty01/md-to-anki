set res to do shell script "
PATH=/opt/homebrew/bin/:$PATH; 
eval `pyenv init --path`;
/Users/alexyang/Documents/anki/md-to-anki/examples/runners/md-anki.sh 2>&1"

display dialog res