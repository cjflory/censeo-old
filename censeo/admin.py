
from __future__ import unicode_literals

from django.contrib import admin

from .models import Meeting
from .models import Ticket
from .models import Vote


class TicketInline(admin.TabularInline):
    model = Ticket


class MeetingAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    list_display = ('__unicode__', 'ticket_count', 'voter_count')
    filter_horizontal = ('voters',)
    save_on_top = True


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Vote)
