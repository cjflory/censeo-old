# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

from .generators import generate_user
from ..templatetags.censeo_tags import get_full_name_or_username


class TestCenseoTags(TestCase):

    def setUp(self):
        self.user = generate_user()

    def tearDown(self):
        self.user.delete()

    def test_get_full_name_or_username_no_name(self):
        self.assertEqual(self.user.username, get_full_name_or_username(self.user))

    def test_get_full_name_or_username_with_name(self):
        self.user.first_name = 'Bilbo'
        self.user.last_name = 'Baggins'
        self.user.save(update_fields=['first_name', 'last_name'])
        self.assertEqual('Bilbo Baggins', get_full_name_or_username(self.user))
