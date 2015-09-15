from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from efinance.models import *
from students.models import *
from efinance.forms import *



class Honorarios2Inline(admin.StackedInline):
    model = Honorarios2

class HonorariosInline(admin.StackedInline):
    model = Honorarios


class EmpleadoAdmin(UserAdmin):

    form = EmpleadoChangeForm
    add_form = EmpleadoCreationForm

    inlines = [Honorarios2Inline,] #solo para mostrar en pacc, despues volver a honorarios
    
    fieldsets = (
        (None, {
            'fields': (
                       ('tipo_doc', 'num_doc', 'puesto', 'password', 'email'),
                       ('first_name', 'second_name', 'last_name'),
                       ('sexo', 'fecha_nac'),
                       ('domicilio', 'localidad', 'telefono'),
                       'nacionalidad',
                       'is_active','groups'
                       )
        }),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tipo_doc','puesto','num_doc','password1', 'password2',
              'first_name', 'second_name','last_name','nacionalidad',
              )}
        ),
    )
    list_display = ('last_name', 'puesto')
    ordering = ('num_doc',)

    def save_model(self, request, obj, form, change):
        # Si es owner, preceptor, directora o vice-directora
        # Guardamos como staff
        if obj.puesto == 3 or obj.puesto == 0 or obj.puesto == 4 or obj.puesto == 5:
            obj.is_staff = True

        if obj.puesto == 3:
            obj.is_superuser = True
        obj.save()


class GastoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'fecha', 'importe')


class SueldoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha', 'importe')




admin.site.register(Gasto, GastoAdmin)
admin.site.register(Honorarios)
admin.site.register(Sueldo, SueldoAdmin)
admin.site.register(PagoSueldo)
admin.site.register(Empleado, EmpleadoAdmin)
