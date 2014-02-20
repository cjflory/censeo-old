# -*- coding: utf-8 -*-

from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone

from .managers import MeetingManager


class Constants(object):
    class DateFormat(object):
        LONG = '%A, %b. %d, %Y'

    class DateFormatTemplate(object):
        LONG = 'l, N d, Y'

    STORY_POINTS = (
        (Decimal(0), '0'),
        (Decimal(.5), '1/2'),
        (Decimal(1), '1'),
        (Decimal(2), '2'),
        (Decimal(3), '3'),
        (Decimal(5), '5'),
        (Decimal(8), '8'),
        (Decimal(13), '13'),
        (Decimal(20), '20'),
        (Decimal(40), '40'),
        (Decimal(100), '100'),
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
    story_point = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                      choices=Constants.STORY_POINTS)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.id)

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)


class Vote(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='user_votes')
    ticket = models.ForeignKey(Ticket, related_name='ticket_votes')
    story_point = models.DecimalField(max_digits=5, decimal_places=2,
                                      choices=Constants.STORY_POINTS)

    class Meta:
        unique_together = ('user', 'ticket')

    def __unicode__(self):
        return u'{}: {} voted {}'.format(
            self.ticket.id,
            self.user.get_full_name(),
            self.get_story_point_display()
        )
