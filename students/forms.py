# -*- encoding: utf-8 -*-

from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.admin import widgets
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab
from tinymce.widgets import TinyMCE

from students.models import Alumno, Informe, Maestra, AlumnoSala, Sala
from finance.models import ServicioSuscripto
from datetime import date

import pdb


class SalaCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            'Salas',
            'sala',
            'turno',
            'seccion',
            'anio_lectivo',
            Field('fecha_inicio', css_class="datepicker"),
            'capacidad'
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Sala 



ServicioSuscriptoFormSet = inlineformset_factory(Alumno, ServicioSuscripto, extra=1, can_delete=True)
AlumnoSalaFormSet = inlineformset_factory(Alumno, AlumnoSala, extra=1, can_delete=True)




class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno

class InformeForm(ModelForm):

    texto = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Informe
        exclude = ('alumno', 'maestra',)


class MaestraCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given num_doc and
    password.
    """

    def __init__(self, *args, **kargs):
        super(MaestraCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']
        
    class Meta:
        model = Maestra
        exclude = ['username',]


class MaestraChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(MaestraChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']
        
    class Meta:
        model = Maestra
        exclude = ['username',]



class MaestraCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Personal',
                'groups',
                'password',
                'tipo_doc',
                'num_doc',
                'email',
                'first_name',
                'second_name',
                'last_name',
                Field('fecha_nac', css_class="datepicker"),
                'sexo',
                'nacionalidad',
                'domicilio',
                'localidad',
                'telefono',
                'salas',
            )
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Maestra
        exclude = ['is_superuser', 'is_staff', 'is_active', 'is_email_verified', 
                   'date_joined', 'user_permissions', 'last_login','puesto'] 
