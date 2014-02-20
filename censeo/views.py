# -*- coding: utf-8 -*-

import json

from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from .forms import AddTicketForm
from .models import Meeting
from .view_mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'censeo/home.html'


class MeetView(LoginRequiredMixin, TemplateView):
    template_name = 'censeo/meet.html'

    def get_context_data(self, **kwargs):
        context = super(MeetView, self).get_context_data(**kwargs)
        context.update({
            'meeting': Meeting.objects.get_current_meeting(self.request.user),
            'form': AddTicketForm(),
        })
        return context


class AddTicket(LoginRequiredMixin, FormView):
    form_class = AddTicketForm
    template_name = 'censeo/snippets/ticket.html'

    def form_valid(self, form):
        return HttpResponse(render_to_string(self.template_name, {'ticket': form.save()}))

    def form_invalid(self, form):
        return HttpResponse(render_to_string(self.template_name, {'errors': form.errors}))


# class UpdateView(LoginRequiredMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse(self.get_context_data(*args, **kwargs), mimetype='application/json')
#
#     def get_context_data(self, *args, **kwargs):
#         meeting_id = kwargs.get('meeting_id', 0)
#         meeting = get_object_or_404(Meeting, id=meeting_id)
#         context = {'meeting': model_to_dict(meeting)}
#         return json.dumps(context)
