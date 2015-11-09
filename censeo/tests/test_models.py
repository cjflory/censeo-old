# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from mock import patch

from .generators import generate_meeting
from .generators import generate_ticket
from .generators import generate_user
from .generators import generate_vote


class TestBase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.meeting = generate_meeting()
        for i in xrange(5):
            cls.meeting.voters.add(generate_user(username='user{0}'.format(i)))
            generate_ticket(id='LON-111{0}'.format(i), meeting=cls.meeting)

        cls.meeting.save()
        cls.user = cls.meeting.voters.all().first()
        cls.ticket = cls.meeting.tickets.all()[0]
        cls.finished_ticket = cls.meeting.tickets.all()[1]
        for voter in cls.meeting.voters.all():
            generate_vote(user=voter, ticket=cls.finished_ticket)

    @classmethod
    def tearDownClass(cls):
        cls.finished_ticket.ticket_votes.all().delete()
        cls.meeting.voters.all().delete()
        cls.meeting.tickets.all().delete()
        cls.meeting.delete()


class TestMeeting(TestBase, TestCase):

    def test_unicode(self):
        expected = _('Meeting on {}').format(self.meeting.start.strftime('%A, %d-%b-%Y'))
        self.assertEqual(expected, self.meeting.__unicode__())

    def test_voter_count(self):
        self.assertEqual(5, self.meeting.voter_count())

    def test_ticket_count(self):
        self.assertEqual(5, self.meeting.ticket_count())


class TestTicket(TestBase, TestCase):

    def test_unicode(self):
        self.assertEqual('{}'.format(self.ticket.id), self.ticket.__unicode__())

    def test_is_voting_completed_incomplete(self):
        self.assertFalse(self.ticket.is_voting_completed())

    def test_is_voting_completed_complete(self):
        self.assertTrue(self.finished_ticket.is_voting_completed())

    def test_has_user_voted_false(self):
        self.assertFalse(self.ticket.has_user_voted(self.user))

    def test_has_user_voted_true(self):
        self.assertTrue(self.finished_ticket.has_user_voted(self.user))

    def test_get_view_ticket_url(self):
        expected = settings.TICKET_URL.format(ticket_number=self.ticket.id)
        self.assertEqual(expected, self.ticket.get_view_ticket_url())


class TestVote(TestBase, TestCase):

    @patch('censeo.models.get_full_name_or_username', return_value='Bilbo Baggins')
    def test_unicode(self, get_full_name_or_username):
        vote = self.finished_ticket.ticket_votes.all().first()
        expected = _('{}: {} voted {}').format(
            vote.ticket.id,
            'Bilbo Baggins',
            vote.get_story_point_display()
        )
        self.assertEqual(expected, vote.__unicode__())
