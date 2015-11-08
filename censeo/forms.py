
from __future__ import unicode_literals

import re

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Meeting
from .models import Ticket


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('id', 'meeting')

    def clean_id(self):
        id = self.cleaned_data['id'].upper()

        if re.match(r'^{}$'.format(settings.TICKET_REGEX), id):
            return id

        raise forms.ValidationError(_('Invalid ticket id'))


class AddVoterForm(forms.Form):
    voter = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(is_active=True),
        to_field_name='username',
        error_messages={'invalid_choice': _('Invalid username')}
    )
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.all(),
        error_messages={'invalid_choice': _('Invalid meeting id')}
    )

    def clean(self):
        cleaned_data = super(AddVoterForm, self).clean()
        voter, meeting = cleaned_data.get("voter"), cleaned_data.get("meeting")
        if voter and meeting and (meeting.voters.filter(username=voter.username)
                                 or meeting.observers.filter(username=voter.username)):
            raise forms.ValidationError(_('User is already in this meeting'))

        return cleaned_data
