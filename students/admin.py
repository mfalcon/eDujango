from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from students.models import *
from finance.models import ServicioSuscripto, Autorizado, Responsable
from efinance.models import Honorarios2
from .forms import MaestraChangeForm, MaestraCreationForm, InformeForm
from finance.settings import SIN_CUOTA


class ServicioSuscriptoInline(admin.StackedInline):
    model = ServicioSuscripto

    fieldsets = (
        (None, {
            'fields': ((('tipo','importe')))
            }),
    )
'''
class AutorizadoInline(admin.StackedInline):
    model = Autorizado

'''

#class ResponsableInline(admin.StackedInline):
    #model = Responsable.alumnos.through

class AlumnoSalaInline(admin.TabularInline):
    model = AlumnoSala
    extra = 2


class AlumnoAdmin(admin.ModelAdmin):
    inlines = [ServicioSuscriptoInline, AlumnoSalaInline,] # ResponsableInline,]
    fieldsets = (
        ('Informacion Personal', {
            'fields': (
                       ('apellido', 'nombre1', 'nombre2'),
                       ('tipo_doc', 'num_doc'),
                       ('sexo', 'fecha_nac'),
                       ('domicilio', 'localidad', 'telefono'),
                       'responsables',
                       'autorizados'
                       )
        }),
        ('Informacion Educacional', {
            'fields': (
                ('fecha_ingreso', 'fecha_egreso'),
                'expresion_verbal',
                'vocabulario'
            )
        }),
        ('Informacion Medica', {
            'fields': (
                        ('padece_enfermedad', 'tipo_enfermedad'),
                        ('controla_esfinteres', 'edad_controla_esfinteres','usa_mamadera'),
                        ('es_alergico', 'toma_medicacion'),
                        ('en_tratamiento_medico', 'detalle_tratamiento'),
                        ('tiene_convulsiones', 'tiene_antitetanica'),
                        'observaciones_medicas',
                        'traslado_emergencia', 'telefono_emergencia',
                      )
        }),
    )
    list_display = ('apellido', 'nombre1')
    list_filter = ('sala', 'fecha_ingreso')
    search_fields = ['apellido']
    actions = ['generar_cuotas']
    
    #TODO: estoy utilizando finance.utils.generate_payments modificado para solo actualizar los alumnos seleccionados
    def generar_cuotas(self, request, queryset):
        '''amount = 0
        #Analiza si debe crear las cuotas del mes actual.
        today = date.today()
        today_tuple = (today.year, today.month)
        # hacer un get y no un filter(ahorro de queries)
        c = Cuota.objects.filter(fecha__month=today.month, fecha__year=today.year)
        cant_cuotas = 0
        if not c and today.month not in SIN_CUOTA:
            students = queryset
            for student in students:
                services = ServicioSuscripto.objects.filter(alumno=student)
                for service in services:
                    amount += service.importe
                c = Cuota(alumno=student, importe=amount, deuda=amount, fecha=today)
                c.save()
                cant_cuotas += 1
                amount = 0'''
        #self.message_user(request, "Se han generado %d cuotas." % cant_cuotas)
        self.message_user(request, "fasafsfsafsasaf")
        
    generar_cuotas.short_description = "Generar las cuotas del mes para los alumnos seleccionados"

    
class HonorariosInline(admin.StackedInline):
    model = Honorarios2


class MaestraAdmin(UserAdmin):

    form = MaestraChangeForm
    add_form = MaestraCreationForm

    inlines = [HonorariosInline,]
    fieldsets = (
        (None, {
            'fields':
                ('password','last_name', ('first_name', 'second_name',),
                       ('tipo_doc', 'num_doc',),
                       'sexo', 'fecha_nac',
                       ('domicilio', 'localidad', 'telefono',),
                        'email', 'salas', 'puesto')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tipo_doc','num_doc', 'puesto','salas','password1', 'password2',
              'first_name', 'second_name','last_name','nacionalidad',
              )}
        ),
    )
    list_display = ('num_doc','last_name', 'first_name')
    #list_display_links = ('nombre',)
    search_fields = ['last_name']
    ordering = ('last_name',)


class SalaAdmin(admin.ModelAdmin):
    #inlines = (AlumnoSalaInline,)
    list_display = ('sala', 'turno')
    

class InformeAdmin(admin.ModelAdmin):
    form = InformeForm
    
    class Admin:
        js = ('js/tiny_mce/tiny_mce.js',
            'js/tiny_mce/textareas.js',
        )


admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Maestra, MaestraAdmin)
admin.site.register(Informe, InformeAdmin)
