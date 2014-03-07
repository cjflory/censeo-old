
from __future__ import unicode_literals

from django.conf import settings

from .models import Constants


def constants(request):
    return {
        'TICKET_MASK_DEFINITIONS': settings.TICKET_MASK_DEFINITIONS,
        'TICKET_MASK': settings.TICKET_MASK,
        'DATE_FORMAT': Constants.DateFormatTemplate,
        'STORY_POINTS': Constants.STORY_POINTS,
    }
