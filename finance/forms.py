# -*- encoding: utf-8 -*-

from django import forms
from django.forms import ModelForm, DateInput
from django.contrib.admin import widgets
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from crispy_forms.bootstrap import TabHolder, Tab

from finance.models import Pago, ServicioSuscripto, UnicoPago, Responsable, Autorizado
from finance.models import CustomUser, Cuota

from datetime import date
import pdb



class CuotaCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('alumno'),
        Field('importe'),
        Field('deuda'),
        Field('fecha', css_class="datepicker"),
        Field('paga'),
        Field('concepto'),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Cuota


class AutorizadoCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Personal',
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
                'telefono'
                
            ),
            Tab(
                'Relación',
                'relacion',
                'otra'
            )
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Autorizado
        exclude = ['is_superuser', 'is_staff', 'is_active', 'is_email_verified', 
                   'date_joined', 'groups', 'user_permissions', 'last_login'] 
                   

class ResponsableCrispyForm(ModelForm):

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Personal',
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
                'telefono'
                
            ),
            Tab(
                'Relación',
                'relacion',
                'ocupacion',
                'telefono_laboral1',
                'telefono_laboral2',
                'como_conocio'
            )
        ),
        ButtonHolder(
            Submit('submit', 'Guardar', css_class='button white')
        )
    )
 
    class Meta:
        model = Responsable
        exclude = ['is_superuser', 'is_staff', 'is_active', 'is_email_verified', 
                   'date_joined', 'groups', 'user_permissions', 'last_login'] 


class ServicioSuscriptoForm(ModelForm):
    class Meta:
        model = ServicioSuscripto
        exclude = ('alumno',)

    def __init__(self, *args, **kwargs):
        # TODO solo mostrar para elegir los tipos que no se crearon actualmente
        self.student = kwargs.pop('st')
        super(ServicioSuscriptoForm, self).__init__(*args, **kwargs)
        '''
        ss = ServicioSuscripto.objects.filter(alumno=student)
        tipo_servicios = []
        for s in ss:
            tipo_servicios += ServicioSuscripto.objects.exclude(alumno=student, tipo=s.tipo)

        pdb.set_trace()
        self.fields['tipo'].queryset = servicios
        '''

    def clean_tipo(self):
        tipo = self.cleaned_data['tipo']
        t = ServicioSuscripto.objects.filter(tipo=tipo, alumno=self.student)
        if t:
            raise forms.ValidationError(_("Ya ha ingresado ese tipo de servicio para este alumno"))
        return self.cleaned_data['tipo']


class PagoForm(ModelForm):
    class Meta:
        model = Pago
        exclude = ('alumno',)
        widgets = { 'fecha': DateInput }

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student')
        super(PagoForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].queryset = Responsable.objects.filter(alumnos=self.student)
        self.fields["responsable"].initial = Responsable.objects.filter(alumnos=self.student)[0]

    def clean_abona(self):
        abona = self.cleaned_data['abona']
        debt = sum(self.student.get_deuda())
        # TODO restar en deuda a unicopago/cuota
        if abona < 0:
            raise forms.ValidationError(_("ERROR: Solo montos positivos por favor"))
        # TODO : puede ser que el padre quiera abonar mas de lo que debe
        if abona > debt:
            raise forms.ValidationError(_("ERROR: No se puede abonar mas de lo que se debe"))

        return self.cleaned_data['abona']


class UnicoPagoForm(ModelForm):
    class Meta:
        model = UnicoPago
        exclude = ('alumno', 'paga', 'deuda')

    def __init__(self, *args, **kwargs):
        # TODO solo mostrar para elegir los tipos que no se crearon actualmente
        self.student = kwargs.pop('st')
        super(UnicoPagoForm, self).__init__(*args, **kwargs)
        self.fields['responsable'].queryset = Responsable.objects.filter(alumnos=self.student)
        self.fields["responsable"].initial = Responsable.objects.filter(alumnos=self.student)[0]

    def clean_tipo(self):
        tipopu = self.cleaned_data['tipo']
        if tipopu.tipo == 0:
            t = UnicoPago.objects.filter(tipo=tipopu, alumno=self.student)
            if t:
                raise forms.ValidationError(_("Ya ha ingresado el pago de matricula"))
        return self.cleaned_data['tipo']






class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given num_doc and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser