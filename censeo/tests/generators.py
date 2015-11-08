# -*- coding: utf-8 -*-

import random
import string

from django.contrib.auth import get_user_model

from ..models import Constants
from ..models import Meeting
from ..models import Ticket
from ..models import Vote


def generate_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in xrange(size))


def generate_email():
    return '{0}@{1}.com'.format(generate_string(), generate_string())


def generate_user(**kwargs):
    user_kwargs = {
        'username': generate_string(),
        'email': generate_email(),
        'password': generate_string()
    }
    user_kwargs.update(kwargs)
    return get_user_model().objects.create_user(
        username=user_kwargs.pop('username'),
        email=user_kwargs.pop('email'),
        password=user_kwargs.pop('password'),
        **user_kwargs
    )


def generate_meeting(**kwargs):
    meeting_kwargs = {}
    meeting_kwargs.update(kwargs)
    return Meeting.objects.create(**meeting_kwargs)


def generate_ticket(**kwargs):
    ticket_kwargs = {
        'id': 'LON-1234',
        'meeting': kwargs.get('meeting') or generate_meeting(),
    }
    ticket_kwargs.update(kwargs)
    return Ticket.objects.create(**ticket_kwargs)


def generate_vote(**kwargs):
    vote_kwargs = {
        'user': kwargs.get('user') or generate_user(),
        'ticket': kwargs.get('ticket') or generate_ticket(),
        'story_point': kwargs.get('story_point') or random.choice(Constants.STORY_POINTS)[0]
    }
    vote_kwargs.update(kwargs)
    return Vote.objects.create(**vote_kwargs)
