# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class MeetingManager(models.Manager):

    def get_current_meeting(self, user):
        now = timezone.now()
        min, max = now - relativedelta(hours=12), now + relativedelta(hours=12)
        meeting, created = self.get_or_create(start__range=(min, max))

        # Check if the user is already set as a voter or observer for the meeting
        is_voter = meeting.voters.filter(username=user.username).exists()
        is_observer = meeting.observers.filter(username=user.username).exists()
        if not is_voter and not is_observer:
            # User should initially be added as a voter
            meeting.voters.add(user)

        return meeting
