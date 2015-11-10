# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext_lazy as _


class Command(NoArgsCommand):
    help = _('Erase the current database and setup a new one')
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
                self.stdout.write(_('Deleted the SQLite database'))

            # Setup the new database
            call_command('migrate', interactive=False)
            self.add_initial_users()

        divider = '==========================================================================='
        self.stdout.write(_(
            "\n{}\n  The following users were added with a temporary password of '{}':"
            "\n    {}\n\n  DON'T FORGET TO CHANGE THESE PASSWORDS!!!\n{}\n\n"
        ).format(
            divider,
            self.default_password,
            '\n    '.join([user['username'] for user in self.users]),
            divider
        ))

    def add_initial_users(self):
        for user_data in self.users:
            user = get_user_model().objects.create_user(user_data['username'], user_data['email'],
                                                        self.default_password)
            user.is_superuser = user_data['superuser']
            user.is_staff = user_data['staff']
            user.first_name = user_data['firstname']
            user.last_name = user_data['lastname']
            user.save()
