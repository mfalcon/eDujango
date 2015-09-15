# Importaciones Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms

# Importaciones de Terceros
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab

# Importaciones Propias
from .models import AlumnoColegio, Profesor



class ProfesorCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Profesor',
                'tipo_doc',
                'num_doc',
                'password',
                'groups',
                'email',
                'first_name',
                'second_name',
                'last_name',
                Field('fecha_nac', css_class="datepicker"),
                'sexo',
                'nacionalidad',
                'localidad',
                'domicilio',
                'telefono',
                'materias'
            )
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Profesor
        exclude = ['last_login','date_joined']


class AlumnoColegioCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Alumno',
                'tipo_doc',
                'num_doc',
                'password',
                'email',
                'first_name',
                'second_name',
                'last_name',
                Field('fecha_nac', css_class="datepicker"),
                'sexo',
                'nacionalidad',
                'localidad',
                'domicilio',
                'telefono',
                'division',
            )
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = AlumnoColegio
        exclude = ['last_login','date_joined']


class AlumnoColegioCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given num_doc and
    password.
    """

    def __init__(self, *args, **kargs):
        super(AlumnoColegioCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']
        
    class Meta:
        model = AlumnoColegio
        exclude = ['username',]


class AlumnoColegioChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(AlumnoColegioChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = AlumnoColegio
        exclude = ['username',]


class ProfesorCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given num_doc and
    password.
    """

    def __init__(self, *args, **kargs):
        super(ProfesorCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']
        
    class Meta:
        model = Profesor
        exclude = ['username',]


class ProfesorChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(ProfesorChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = Profesor
        exclude = ['username',]