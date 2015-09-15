from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from finance.models import *
from finance.forms import *
#from students.models import Alumno


class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'importe')

class CuotaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'importe', 'fecha')

class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'abona', 'fecha')

class TipoUnicoPagoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'importe')

class ItemPagoAdmin(admin.ModelAdmin):
    pass


class AutorizadoAdmin(admin.ModelAdmin):
    #inlines = [AlumnoInline]

    fieldsets = (
        (None, {
            'fields': (('last_name','relacion'), ('first_name', 'second_name',),
                       ('tipo_doc', 'num_doc'),
                       'sexo', 'fecha_nac','otra',
                       ('domicilio', 'localidad', 'telefono',),
                        'email',),
        }),
    )
    list_display = ('last_name', 'first_name')
    #list_display_links = ('nombre',)
    search_fields = ['last_name']


class ResponsableAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': (('password'), ('first_name', 'second_name','last_name'),
                       ('tipo_doc', 'num_doc'),
                       ('sexo','fecha_nac','ocupacion'),
                       ('domicilio', 'localidad', 'telefono','telefono_laboral1','telefono_laboral2'),
                        'email','como_conocio'),
        }),
    )
    list_display = ('last_name', 'first_name')
    #list_display_links = ('nombre',)
    search_fields = ['last_name']



admin.site.register(Cuota, CuotaAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(ItemPago, ItemPagoAdmin)
admin.site.register(ServicioSuscripto)
admin.site.register(TipoServicio, TipoServicioAdmin)
admin.site.register(UnicoPago)
admin.site.register(TipoUnicoPago, TipoUnicoPagoAdmin)
admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Autorizado,AutorizadoAdmin)




class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('num_doc', 'fecha_nac', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('num_doc','email', 'password')}),
        ('Personal info', {'fields': ('fecha_nac','first_name','second_name','last_name',
            'tipo_doc','sexo','nacionalidad','telefono','domicilio','localidad',)}),
        ('Permissions', {'fields': ('is_staff','is_active','is_email_verified','date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('num_doc','password1', 'password2')}
        ),
    )
    search_fields = ('num_doc',)
    ordering = ('num_doc',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)