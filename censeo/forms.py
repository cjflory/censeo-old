
from __future__ import unicode_literals

import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Ticket


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('id', 'meeting')

    def clean_id(self):
        id = self.cleaned_data['id'].upper()

        if re.match(r'^LON-\d{4}$', id):
            return id

        raise forms.ValidationError(_('Invalid ticket ID.'))
