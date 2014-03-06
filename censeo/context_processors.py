
from __future__ import unicode_literals

from .models import Constants


def constants(request):
    return {
        'DATE_FORMAT': Constants.DateFormatTemplate,
        'STORY_POINTS': Constants.STORY_POINTS,
    }
