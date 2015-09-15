# Improtaciones Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Improtaciones Propias
from .models import AlumnoColegio, Profesor, Materia, Division, MateriaDivision, Calificacion, Asistencia, EstadoAsistencia
from .forms import AlumnoColegioChangeForm, AlumnoColegioCreationForm, ProfesorChangeForm, ProfesorCreationForm





class AlumnoColegioAdmin(UserAdmin):
    form = AlumnoColegioChangeForm
    add_form = AlumnoColegioCreationForm

    fieldsets = (
        (None, {
            'fields': (
                       ('tipo_doc', 'num_doc', 'password', 'email'),
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
            'fields': ('tipo_doc','num_doc','password1', 'password2',
              'first_name', 'second_name','last_name','nacionalidad','division',
              )}
        ),
    )
    list_display = ('first_name','last_name',)
    ordering = ('num_doc',)


class ProfesorAdmin(UserAdmin):
    form = ProfesorChangeForm
    add_form = ProfesorCreationForm

    fieldsets = (
        (None, {
            'fields': (
                       ('tipo_doc', 'num_doc', 'password', 'email'),
                       ('first_name', 'second_name', 'last_name'),
                       ('materias'),
                       ('sexo', 'fecha_nac'),
                       ('domicilio', 'localidad', 'telefono'),
                       'nacionalidad',
                       'is_active','groups','user_permissions'
                       )
        }),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tipo_doc','num_doc','password1', 'password2',
              'first_name', 'second_name','last_name','nacionalidad',
              )}
        ),
    )
    list_display = ('last_name',)
    ordering = ('num_doc',)



admin.site.register(AlumnoColegio, AlumnoColegioAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Division)
admin.site.register(MateriaDivision)
admin.site.register(Materia)
admin.site.register(Asistencia)
admin.site.register(Calificacion)
admin.site.register(EstadoAsistencia)