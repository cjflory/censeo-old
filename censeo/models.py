# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import MeetingManager
from .templatetags.censeo_tags import get_full_name_or_username


class Constants(object):
    class DateFormat(object):
        LONG = '%A, %b. %d, %Y'

    class DateFormatTemplate(object):
        LONG = 'l, N d, Y'

    STORY_POINTS = (
        (0.0, _('0')),
        (0.5, _('1/2')),
        (1.0, _('1')),
        (2.0, _('2')),
        (3.0, _('3')),
        (5.0, _('5')),
        (8.0, _('8')),
        (13.0, _('13')),
        (20.0, _('20')),
        (40.0, _('40')),
        (100.0, _('100')),
    )


class Meeting(models.Model):
    notes = models.TextField(blank=True, null=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meetings_as_voter', blank=True)
    observers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meetings_as_observer', blank=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    objects = MeetingManager()

    def __unicode__(self):
        return _('Meeting on {}').format(self.start.strftime('%A, %d-%b-%Y'))

    def voter_count(self):
        return self.voters.count()
    voter_count.short_description = _('# of Voters')

    def ticket_count(self):
        return self.tickets.count()
    ticket_count.short_description = _('# of Tickets')


class Ticket(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    meeting = models.ForeignKey(Meeting, related_name='tickets')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.id)

    def is_voting_completed(self):
        return self.ticket_votes.count() == self.meeting.voters.count()

    def has_user_voted(self, user):
        is_observer = self.meeting.observers.filter(username=user.username).exists()
        return is_observer or self.ticket_votes.filter(user=user).exists()

    def get_view_ticket_url(self):
        return settings.TICKET_URL.format(ticket_number=self.id)


class Vote(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_votes')
    ticket = models.ForeignKey(Ticket, related_name='ticket_votes')
    story_point = models.FloatField(choices=Constants.STORY_POINTS)

    class Meta:
        unique_together = ('user', 'ticket')

    def __unicode__(self):
        return _('{}: {} voted {}').format(
            self.ticket.id,
            get_full_name_or_username(self.user),
            self.get_story_point_display()
        )
