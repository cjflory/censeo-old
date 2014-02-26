# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag()
def get_full_name_or_username(user):
    return user.get_full_name() or user.username
