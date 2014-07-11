# Censeo

Censeo is an app that will help simplify your team's story pointing meetings.

### Usage

1. Register for an account if you don't already have one.

1. Login and join the meeting.  A continuously updated list of voters in the meeting will be
displayed.  Votes for a ticket will not be visible until all voters have voted on that ticket.

1. Quickly add tickets to the meeting.  When no tickets are currently selected, the ticket list
will remain up to date with all tickets added.

1. Click on a ticket to vote or see its results.  When a ticket is selected, the list of tickets
stops automatically updating, and the voting results for that ticket begin to update automatically.
Click on the same ticket again to de-select it, stop the automatic updates for voting results, and
restart the automatic updates to the ticket list.

### Dependencies

* git
* npm
* virtualenv
* virtualenvwrapper

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

1. Navigate to http://0.0.0.0:8000/ (_default username is **myuser**, default password is **asdfasdf**_)

### TODO

* Add more tests
