# -*- coding: utf-8 -*-

from .models import Constants


def constants(request):
    return {
        'DATE_FORMAT': Constants.DateFormatTemplate,
        'STORY_POINTS': Constants.STORY_POINTS,
        # TODO:  Find a better place for this?
        'DEFAULT_VOTING_HTML': '<div class="text-center">Select a ticket to vote on</div>',
    }
