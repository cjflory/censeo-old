# -*- coding: utf-8 -*-

import json

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import TemplateView

from .forms import AddTicketForm
from .mixins import AjaxRequiredMixin
from .mixins import LoginRequiredMixin
from .mixins import LoginRequiredNoRedirectMixin
from .models import Meeting
from .models import Ticket
from .models import Vote


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


class RegisterNewUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register_user.html'

    def form_valid(self, form):
        self.object = form.save()

        authed_user = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password1'])
        login(self.request, authed_user)
        return super(RegisterNewUserView, self).form_valid(form)

    def get_success_url(self):
        return reverse('meet')


class BaseAjaxView(LoginRequiredNoRedirectMixin, AjaxRequiredMixin):
    pass


class AddTicketView(BaseAjaxView, FormView):
    form_class = AddTicketForm
    template_name = 'censeo/snippets/ticket.html'

    def form_valid(self, form):
        return HttpResponse(render_to_string(self.template_name, {'ticket': form.save()}))

    def form_invalid(self, form):
        return HttpResponse(json.dumps({'errors': form.errors}), content_type="application/json")


class BasePollView(BaseAjaxView, TemplateView):
    """ Base view for views that handle meeting polling """

    def get_queryset(self, **kwargs):
        meeting = get_object_or_404(Meeting, id=kwargs['meeting_id'])
        return getattr(meeting, self.meeting_attr).all()

    def get_context_data(self, **kwargs):
        context = super(BasePollView, self).get_context_data(**kwargs)
        context[self.context_key] = self.get_queryset(**kwargs)
        return context


class PollTicketsView(BasePollView):
    template_name = 'censeo/snippets/tickets.html'
    context_key = 'tickets'
    meeting_attr = 'tickets'


class PollUsersView(BasePollView):
    template_name = 'censeo/snippets/users.html'
    context_key = 'users'
    meeting_attr = 'voters'


class TicketVotingBaseView(BaseAjaxView, TemplateView):
    template_name = 'censeo/snippets/voting.html'

    def get_context_data(self, **kwargs):
        context = super(TicketVotingBaseView, self).get_context_data(**kwargs)
        context['selected_ticket'] = get_object_or_404(Ticket, id=kwargs.get('ticket_id'))
        return context

    def get_vote_context(self, ticket):
        vote_context = {}
        all_votes = ticket.ticket_votes.all()

        if ticket.is_voting_completed():
            # Ticket has already been voted on
            vote_context['votes'] = all_votes
            vote_context['all_voted'] = True
        elif ticket.has_user_voted(self.request.user):
            # Ticket is currently being voted on
            vote_context['votes'] = all_votes
        else:
            # Allow user to vote
            vote_context['voting'] = True

        return vote_context


class GetTicketVotesView(TicketVotingBaseView):

    def get_context_data(self, **kwargs):
        context = super(GetTicketVotesView, self).get_context_data(**kwargs)
        context.update(self.get_vote_context(context['selected_ticket']))
        return context


class VoteOnTicketView(TicketVotingBaseView):

    def get_users_vote(self, **kwargs):
        """ Get the users vote from the kwargs, and make sure it's valid """
        try:
            users_vote = float(kwargs['vote'])
        except ValueError:
            users_vote = None

        return users_vote

    def get_context_data(self, **kwargs):
        context = super(VoteOnTicketView, self).get_context_data(**kwargs)

        users_vote = self.get_users_vote(**kwargs)
        if users_vote is None:
            # Users vote is invalid, pretend user hasn't voted
            context['voting'] = True
        else:
            # Users vote is valid
            vote = Vote(
                user=self.request.user,
                ticket=context['selected_ticket'],  # validated with get_object_or_404
                story_point=users_vote
            )
            vote.save()
            context.update(self.get_vote_context(context['selected_ticket']))

        return context
