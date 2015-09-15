from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.admin import widgets

from eventos.models import Noticia2

from datetime import date

class NoticiaForm(ModelForm):
    class Meta:
        model = Noticia2
