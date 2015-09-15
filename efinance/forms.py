# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, DateInput, PasswordInput
from django.contrib.admin import widgets
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import TabHolder, Tab

from efinance.models import PagoSueldo, Gasto, Empleado, Sueldo, Client
from datetime import date



class PagoSueldoCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            'Pago de Sueldo',
            'empleado',
            'abona',
            Field('fecha', css_class="datepicker"),
            'comentarios'
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = PagoSueldo


class SueldoCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            'Sueldo',
            'empleado',
            'importe',
            Field('fecha', css_class="datepicker"),
            'pago',
            'deuda'
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Sueldo


class GastoCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Fieldset(
            'Gastos',
            'tipo',
            'importe',
            Field('fecha', css_class="datepicker"),
            'pago',
            'comentarios'
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Gasto


class DemoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    dni = forms.IntegerField()
    imagen = forms.ImageField(required=False)
    password1 = forms.CharField(widget=PasswordInput())
    password2 = forms.CharField(widget=PasswordInput())
    datosPrueba = forms.BooleanField(required=False)

    def clean_nombre(self):
        try:
            Client.objects.get(nombre=self.cleaned_data.get("nombre"))
        except Client.DoesNotExist :
            return self.cleaned_data['nombre']
        raise forms.ValidationError("este nombre ya existe")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("Debés confirmar tu contraseña")
        if password1 != password2:
            raise forms.ValidationError("Tus contraseñas no coinciden")
        return password2



class PagoSueldoForm(ModelForm):
    class Meta:
        model = PagoSueldo
        exclude = ('empleado',)
        widgets = { 'fecha': DateInput }
        
    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado')
        super(PagoSueldoForm, self).__init__(*args, **kwargs)
        
    def clean_abona(self):
        abona = self.cleaned_data['abona']
        deuda = self.empleado.get_deuda()
        # TODO restar en deuda a unicopago/cuota
        if abona < 0:
            raise forms.ValidationError(_("Solo montos positivos por favor"))
        # TODO : puede ser que el padre quiera abonar mas de lo que debe
        if abona > deuda:
            raise forms.ValidationError(_("No se puede abonar mas de lo que se debe"))     
        
        return self.cleaned_data['abona']
        
        
class GastoForm(ModelForm):
    class Meta:
        model = Gasto


class EmpleadoCrispyForm(ModelForm):

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
                'puesto',
                
            )
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Empleado
        exclude = ['is_superuser', 'is_staff', 'is_active', 'is_email_verified', 
                   'date_joined', 'user_permissions', 'last_login'] 

class EmpleadoCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given num_doc and
    password.
    """

    def __init__(self, *args, **kargs):
        super(EmpleadoCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']
        
    class Meta:
        model = Empleado
        exclude = ['username',]


class EmpleadoChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(EmpleadoChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = Empleado
        exclude = ['username',]