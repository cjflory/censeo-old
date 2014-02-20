# -*- coding: utf-8 -*-

from .models import Constants


def constants(request):
    return {'DATE_FORMAT': Constants.DateFormatTemplate}
