
from __future__ import unicode_literals
import json

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

from .forms import AddTicketForm
from .forms import AddVoterForm
from .mixins import AjaxRequiredMixin
from .mixins import LoginRequiredMixin
from .mixins import LoginRequiredNoRedirectMixin
from .models import Meeting
from .models import Ticket
from .models import Vote

User = get_user_model()


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


class UserSearchView(BaseAjaxView, ListView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'censeo/snippets/user_autocomplete.txt'

    def get_queryset(self):
        queryset = super(UserSearchView, self).get_queryset()
        meeting_id = self.kwargs['meeting_id']
        term = self.request.GET.get('term')

        # Filter the queryset by the search term & meeting id
        queryset = queryset.filter(
            Q(username__icontains=term) |
            Q(first_name__icontains=term) |
            Q(last_name__icontains=term) |
            Q(email__icontains=term)
        ).exclude(
            Q(meetings_as_voter__id=meeting_id) |
            Q(meetings_as_observer__id=meeting_id)
        )

        return queryset


class BaseAjaxFormView(BaseAjaxView, FormView):

    def form_invalid(self, form):
        return HttpResponse(json.dumps({'errors': form.errors}), content_type="application/json")


class AddTicketView(BaseAjaxFormView):
    form_class = AddTicketForm
    template_name = 'censeo/snippets/ticket.html'

    def form_valid(self, form):
        return HttpResponse(render_to_string(self.template_name, {
            'ticket': form.save()
        }, context_instance=RequestContext(self.request)))


class AddVoterView(BaseAjaxFormView):
    form_class = AddVoterForm
    template_name = 'censeo/snippets/voter.html'

    def form_valid(self, form):
        # Validation has already happened
        voter = form.cleaned_data['voter']
        meeting = form.cleaned_data['meeting']
        meeting.voters.add(voter)
        return HttpResponse(render_to_string(self.template_name, {
            'voter': voter,
            'meeting': meeting,
        }, context_instance=RequestContext(self.request)))


class RemoveTicketView(BaseAjaxView, DeleteView):
    model = Ticket
    pk_url_kwarg = 'ticket_id'

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        return super(RemoveTicketView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse(status=204)


class BaseMeetingAjaxView(BaseAjaxView, DetailView):
    """ Base view for views that pass meeting_id as a url kwarg """
    context_object_name = 'meeting'
    model = Meeting
    pk_url_kwarg = 'meeting_id'


class PollTicketsView(BaseMeetingAjaxView):
    template_name = 'censeo/snippets/tickets.html'

    def get_context_data(self, **kwargs):
        context = super(PollTicketsView, self).get_context_data(**kwargs)
        context['tickets'] = context['meeting'].tickets.all()
        return context


class PollUsersView(BaseMeetingAjaxView):
    template_name = 'censeo/snippets/users.html'

    def get_context_data(self, **kwargs):
        context = super(PollUsersView, self).get_context_data(**kwargs)
        context['voters'] = context['meeting'].voters.all()
        context['observers'] = context['meeting'].observers.all()
        return context


class BecomeObserverView(BaseMeetingAjaxView):
    """ View to switch the user from a voter to an observer in the meeting """
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        meeting = self.get_object()
        meeting.voters.remove(self.request.user)
        meeting.observers.add(self.request.user)

        return HttpResponse(status=204)


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


class ResetTicketVotesView(BaseAjaxView, DeleteView):
    model = Ticket
    pk_url_kwarg = 'ticket_id'

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        return super(ResetTicketVotesView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()
        if not ticket.is_voting_completed():
            return HttpResponseBadRequest()

        ticket.ticket_votes.all().delete()
        return HttpResponse(status=204)


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
