from django import forms
from django.utils.translation import ugettext_lazy as _
from schedule.models import Event, Occurrence
import datetime
import time


class SpanForm(forms.ModelForm):

    start = forms.DateTimeField(label=_("Comienzo"),
                                widget=forms.SplitDateTimeWidget)
    end = forms.DateTimeField(label=_("Fin"),
                              widget=forms.SplitDateTimeWidget, help_text = _("El fin debe ser posterior al comienzo."))

    def clean_end(self):
        if self.cleaned_data['end'] <= self.cleaned_data['start']:
            raise forms.ValidationError(_("El fin debe ser posterior al comienzo."))
        return self.cleaned_data['end']


class EventForm(SpanForm):
    def __init__(self, hour24=False, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
    
    end_recurring_period = forms.DateTimeField(label=_("Fin del periodo recurrente"),
                                               help_text = _("Esta fecha es ignorada para eventos de una sola ocurrencia."), required=False)
    
    class Meta:
        model = Event
        exclude = ('creator', 'created_on', 'calendar')
        

class OccurrenceForm(SpanForm):
    
    class Meta:
        model = Occurrence
        exclude = ('original_start', 'original_end', 'event', 'cancelled')
