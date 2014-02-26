# -*- coding: utf-8 -*-

from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden


def ajax_required(view):
    """ AJAX request required decorator """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return view(request, *args, **kwargs)

    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__

    return wrap


def login_required_no_redirect(view_func):
    """
    This decorator verifies the user is logged in, and returns HttpResponseForbidden() if they
    aren't. This should typically be used for AJAX views, so the login page isn't returned.
    """

    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return decorated
