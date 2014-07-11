# -*- coding: utf-8 -*-

from django import forms
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from .generators import generate_meeting
from ..forms import AddTicketForm


class TestAddTicketForm(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.meeting = generate_meeting()
        cls.Form = AddTicketForm

    @classmethod
    def tearDownClass(cls):
        cls.meeting.delete()

    def test_required_fields(self):
        """ Verify the list of form fields that should always be required. """
        form = self.Form(data={})
        self.assertFalse(form.is_valid())

        # Verify the correct set of fields caused errors because they are required
        required_error = ['This field is required.']
        self.assertEqual({
            'id': required_error,
            'meeting': required_error,
        }, form.errors)

    def test_clean_id_invalid(self):
        form = self.Form(data={'id': 'foo', 'meeting': self.meeting.id})
        self.assertFalse(form.is_valid())
        self.assertEqual(['Invalid ticket id'], form.errors['id'])

    def test_clean_id_valid(self):
        form = self.Form(data={'id': 'LON-1111', 'meeting': self.meeting.id})
        self.assertTrue(form.is_valid())
