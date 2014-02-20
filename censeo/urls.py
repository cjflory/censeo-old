from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

from .views import AddTicket
from .views import HomeView
from .views import MeetView
# from .views import UpdateView

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'censeo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    # url(r'^update/(?P<meeting_id>\d+)/', UpdateView.as_view(), name='update'),
    url(r'^ticket/add$', AddTicket.as_view(), name='add_ticket'),
    url(r'^meet$', MeetView.as_view(), name='meet'),
    url(r'^$', HomeView.as_view(), name='home'),
)
