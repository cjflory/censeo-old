# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .decorators import ajax_required
from .decorators import login_required_no_redirect


class LoginRequiredMixin(object):
    """ Mixin to require user to be logged in """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class LoginRequiredNoRedirectMixin(object):
    """ Mixin to require user to be logged in, but doesn't redirect to the login page """

    @method_decorator(login_required_no_redirect)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredNoRedirectMixin, self).dispatch(*args, **kwargs)


class AjaxRequiredMixin(object):
    """ Mixin to require AJAX """

    @method_decorator(ajax_required)
    def dispatch(self, *args, **kwargs):
        return super(AjaxRequiredMixin, self).dispatch(*args, **kwargs)
