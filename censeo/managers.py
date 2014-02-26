# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta


class MeetingManager(models.Manager):

    def get_current_meeting(self, user):
        now = timezone.now()
        min, max = now - relativedelta(hours=12), now + relativedelta(hours=12)
        meeting, created = self.get_or_create(start__range=(min, max))
        if not meeting.voters.filter(username=user.username).first():
            meeting.voters.add(user)

        return meeting
