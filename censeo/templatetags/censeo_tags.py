# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def jsonify(value, indent=None):
    """ Filter for encoding python objects to JSON (use the 'indent' param to make it pretty) """
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder, indent=indent))


@register.simple_tag()
def get_full_name_or_username(user):
    return user.get_full_name() or user.username
