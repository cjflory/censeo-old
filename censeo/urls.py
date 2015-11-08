
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from .views import AddTicketView
from .views import AddVoterView
from .views import UserSearchView
from .views import UpdateRoleView
from .views import PollTicketsView
from .views import GetTicketVotesView
from .views import PollUsersView
from .views import HomeView
from .views import MeetView
from .views import RegisterNewUserView
from .views import RemoveTicketView
from .views import ResetTicketVotesView
from .views import VoteOnTicketView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/register$', RegisterNewUserView.as_view(), name='register_new_user'),


    # AJAX URLs
    url(r'^voter/add$', AddVoterView.as_view(), name='add_voter'),

    url(r'^ticket/(?P<ticket_id>{})/vote/(?P<vote>[\d\.]+)$'.format(settings.TICKET_REGEX),
        VoteOnTicketView.as_view(), name='vote_on_ticket'),
    url(r'^ticket/(?P<ticket_id>{})/votes$'.format(settings.TICKET_REGEX),
        GetTicketVotesView.as_view(), name='get_ticket_votes'),
    url(r'^ticket/(?P<ticket_id>{})/votes/reset$'.format(settings.TICKET_REGEX),
        ResetTicketVotesView.as_view(), name='reset_ticket_votes'),
    url(r'^ticket/(?P<ticket_id>{})/remove$'.format(settings.TICKET_REGEX),
        RemoveTicketView.as_view(), name='remove_ticket'),
    url(r'^ticket/add$', AddTicketView.as_view(), name='add_ticket'),

    url(r'^meeting/(?P<meeting_id>\d+)/update-role/(?P<role>(observer|voter))$', UpdateRoleView.as_view(),
        name='update_role'),
    url(r'^meeting/(?P<meeting_id>\d+)/tickets$', PollTicketsView.as_view(), name='poll_tickets'),
    url(r'^meeting/(?P<meeting_id>\d+)/users$', PollUsersView.as_view(), name='poll_users'),
    url(r'^meeting/(?P<meeting_id>\d+)/users/search$', UserSearchView.as_view(),
        name='user_search'),


    # Page URLs
    url(r'^meet$', MeetView.as_view(), name='meet'),
    url(r'^$', HomeView.as_view(), name='home'),
)
