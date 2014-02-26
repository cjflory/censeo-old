#!/bin/bash

clear
echo "---------------------------------------"
echo "Setting up Censeo for local development"
echo "---------------------------------------"
echo ""
echo ""

if [ -z  $1 ]; then
    echo "ERROR:  You must provide a project name"
    echo ""
    exit 0
fi
if [ -z  $WORKON_HOME ]; then
    WORKON_HOME=$HOME/.virtualenvs
fi

if [ -e $WORKON_HOME/$1 ] && [ "$VIRTUAL_ENV" = "" ]; then
    # Virtual environment exists and no active virtual environment
    source $(which virtualenvwrapper.sh)
    workon $1
    cdvirtualenv
elif [ -e $WORKON_HOME/$1 ] && [ "$VIRTUAL_ENV" = "$WORKON_HOME/$1" ]; then
    # Virtual environment exists and is active
    cd $WORKON_HOME/$1
elif [ "$VIRTUAL_ENV" != "" ] && [ "$VIRTUAL_ENV" != "$WORKON_HOME/$1" ]; then
    # A different virtual environment is active (not supported)
    echo ""
    echo "ERROR:  You cannot create a new virtual environment while a different one is active"
    echo '    Run the "deactivate" command, and then try again'
    echo ""
    exit 0
else
    # Virtual environment doesn't exist
    source $(which virtualenvwrapper.sh)
    mkvirtualenv $1
    workon $1
    cdvirtualenv
fi

git clone https://github.com/cjflory/censeo.git src/$1
cd src/$1
git remote rm origin
echo export PYTHONPATH='$VIRTUAL_ENV'/src/$1 >> $VIRTUAL_ENV/bin/postactivate
echo export DJANGO_SETTINGS_MODULE=censeo.settings >> $VIRTUAL_ENV/bin/postactivate
echo export SECRET_KEY='secret-dev-key' >> $VIRTUAL_ENV/bin/postactivate
echo unset PYTHONPATH >> $VIRTUAL_ENV/bin/postdeactivate
echo unset DJANGO_SETTINGS_MODULE >> $VIRTUAL_ENV/bin/postdeactivate
echo unset SECRET_KEY >> $VIRTUAL_ENV/bin/postdeactivate
pip install -r requirements.txt

echo ""
echo ""
echo "------------------------------------------------"
echo "Finished setting up Censeo for local development"
echo ""
echo "    Work on this project:  workon $1"
echo "    Navigate to project root:  cdvirtualenv src/$1/"
echo "    Run the 'db_reset' management command:  django-admin.py db_reset"
echo "------------------------------------------------"
