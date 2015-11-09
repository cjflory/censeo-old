# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden


def ajax_required(view):
    """ AJAX request required decorator """

    def decorated(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return view(request, *args, **kwargs)

    decorated.__doc__ = view.__doc__
    decorated.__name__ = view.__name__

    return decorated


def login_required_no_redirect(view):
    """
    This decorator verifies the user is logged in, and returns HttpResponseForbidden() if they
    aren't. This should typically be used for AJAX views, so the login page isn't returned.
    """

    def decorated(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return view(request, *args, **kwargs)

    decorated.__doc__ = view.__doc__
    decorated.__name__ = view.__name__

    return decorated
