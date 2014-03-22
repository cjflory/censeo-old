
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from .views import AddTicketView
from .views import BecomeObserverView
from .views import PollTicketsView
from .views import GetTicketVotesView
from .views import PollUsersView
from .views import HomeView
from .views import MeetView
from .views import RegisterNewUserView
from .views import ResetTicketVotesView
from .views import VoteOnTicketView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register$', RegisterNewUserView.as_view(), name='register_new_user'),

    # Ticket AJAX URLs
    url(r'^ticket/(?P<ticket_id>{})/vote/(?P<vote>[\d\.]+)$'.format(settings.TICKET_REGEX),
        VoteOnTicketView.as_view(), name='vote_on_ticket'),
    url(r'^ticket/(?P<ticket_id>{})/votes$'.format(settings.TICKET_REGEX),
        GetTicketVotesView.as_view(), name='get_ticket_votes'),
    url(r'^ticket/(?P<ticket_id>{})/votes/reset$'.format(settings.TICKET_REGEX),
        ResetTicketVotesView.as_view(), name='reset_ticket_votes'),
    url(r'^ticket/add$', AddTicketView.as_view(), name='add_ticket'),

    # Meeting AJAX URLs
    url(r'^meeting/(?P<meeting_id>\d+)/become-observer$', BecomeObserverView.as_view(), name='become_observer'),
    url(r'^meeting/(?P<meeting_id>\d+)/tickets$', PollTicketsView.as_view(), name='poll_tickets'),
    url(r'^meeting/(?P<meeting_id>\d+)/users$', PollUsersView.as_view(), name='poll_users'),

    # Page URLs
    url(r'^meet$', MeetView.as_view(), name='meet'),
    url(r'^$', HomeView.as_view(), name='home'),
)
