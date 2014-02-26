# -*- coding: utf-8 -*-

import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Erase the current database and setup a new one'
    default_password = 'asdfasdf'
    users = (
        {'username': 'myuser', 'email': 'me@gmail.com', 'firstname': 'My', 'lastname': 'User',
         'superuser': True, 'staff': True},
        # Add more users here
    )

    def handle_noargs(self, **options):
        if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
            # Delete the SQLite database
            db_path = settings.DATABASES['default']['NAME']
            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write('Deleted the SQLite database')

            # Setup the new database
            call_command('syncdb', interactive=False)
            self.add_initial_users()
            call_command('migrate', 'censeo')

        self.stdout.write(
            "\n{0} initial user(s) added with temporary password of '{1}'\nDON'T FORGET TO "
            "CHANGE THESE PASSWORDS!!!\n\n".format(len(self.users), self.default_password)
        )

    def add_initial_users(self):
        for user_data in self.users:
            user = User.objects.create_user(user_data['username'], user_data['email'],
                                            self.default_password)
            user.is_superuser = user_data['superuser']
            user.is_staff = user_data['staff']
            user.first_name = user_data['firstname']
            user.last_name = user_data['lastname']
            user.save()
