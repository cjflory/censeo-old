# Censeo

A simple scrum poker app.

### Development

To setup Censeo for local development, run the following commands:
> _Replace all occurrences of **&lt;PROJECT NAME&gt;** in the following commands, with the name of your project_

1. This script will setup the virtual environment, clone the repository, and install the requirements:

        curl https://raw.github.com/cjflory/censeo/master/setup_dev.sh | sh -s <PROJECT NAME>

1. Activate the virtual environment and navigate to the project root:

        workon <PROJECT NAME>
        cdvirtualenv src/<PROJECT NAME>

1. Setup the database initially:

        django-admin.py db_reset

1. Start the Django server:

        django-admin.py runserver 0.0.0.0:8000

1. Navigate to http://0.0.0.0:8000/

### TODO

* Write tests
