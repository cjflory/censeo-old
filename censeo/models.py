# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from .managers import MeetingManager


class Constants(object):
    class DateFormat(object):
        LONG = '%A, %b. %d, %Y'

    class DateFormatTemplate(object):
        LONG = 'l, N d, Y'

    STORY_POINTS = (
        (0.0, '0'),
        (0.5, '1/2'),
        (1.0, '1'),
        (2.0, '2'),
        (3.0, '3'),
        (5.0, '5'),
        (8.0, '8'),
        (13.0, '13'),
        (20.0, '20'),
        (40.0, '40'),
        (100.0, '100'),
    )


class Meeting(models.Model):
    notes = models.TextField(blank=True, null=True)
    voters = models.ManyToManyField(User, related_name='meetings_as_voter', blank=True, null=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    objects = MeetingManager()

    def __unicode__(self):
        return u'Meeting on {}'.format(self.start.strftime('%A, %d-%b-%Y'))

    def voter_count(self):
        return self.voters.count()
    voter_count.short_description = '# of Voters'

    def ticket_count(self):
        return self.tickets.count()
    ticket_count.short_description = '# of Tickets'


class Ticket(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    meeting = models.ForeignKey(Meeting, related_name='tickets')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.id)

    def is_voting_completed(self):
        return self.ticket_votes.count() == self.meeting.voters.count()

    def has_user_voted(self, user):
        return self.ticket_votes.filter(user=user).exists()


class Vote(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_votes')
    ticket = models.ForeignKey(Ticket, related_name='ticket_votes')
    story_point = models.FloatField(choices=Constants.STORY_POINTS)

    class Meta:
        unique_together = ('user', 'ticket')

    def __unicode__(self):
        return u'{}: {} voted {}'.format(
            self.ticket.id,
            self.user.get_full_name(),
            self.get_story_point_display()
        )
