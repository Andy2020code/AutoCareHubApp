from django import forms

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'desired_time', 'service_desired', 'street_address', 'zip_code', 'city', 'state']