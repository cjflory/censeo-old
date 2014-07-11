# -*- coding: utf-8 -*-

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .generators import generate_user
from ..models import Meeting

User = get_user_model()


class TestMeetingManager(TestCase):

    def tearDown(self):
        User.objects.all().delete()
        Meeting.objects.all().delete()

    def test_get_current_meeting_none_exist(self):
        """ Verify that the current meeting is created correctly, if it doesn't exist """
        self.assertEqual(0, Meeting.objects.count())

        new_meeting = Meeting.objects.get_current_meeting(generate_user())

        self.assertEqual(1, Meeting.objects.count())
        self.assertEqual([new_meeting], list(Meeting.objects.all()))

    def test_get_current_meeting_exists(self):
        """ Verify that the current meeting is retrieved and not duplicated if it exists """
        user = generate_user()

        existing = Meeting.objects.get_current_meeting(user)
        self.assertEqual(1, Meeting.objects.count())
        self.assertEqual([existing], list(Meeting.objects.all()))

        retrieved = Meeting.objects.get_current_meeting(user)
        self.assertEqual(1, Meeting.objects.count())
        self.assertEqual(existing, retrieved)
