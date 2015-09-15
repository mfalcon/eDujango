# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _

from students.tipos import *
from finance.models import CustomUser, Cuota, UnicoPago, Pago, ServicioSuscripto, Persona
from efinance.models import Empleado
from django.core.urlresolvers import reverse

from datetime import datetime, date



class Alumno(Persona):
    sala = models.ManyToManyField('Sala', through='AlumnoSala', blank=True)

    responsables = models.ManyToManyField('finance.Responsable', related_name='alumnos', blank=True, null=True)
    autorizados = models.ManyToManyField('finance.Autorizado', blank=True, null=True)
    
    #hermanos
    hermanos = models.ManyToManyField('Alumno', blank=True, null=True)

    fecha_ingreso = models.DateField(default=date.today)
    fecha_egreso = models.DateField(blank=True, null=True)

    #medica
    padece_enfermedad = models.BooleanField(default=False)
    tipo_enfermedad = models.CharField(max_length=40, blank=True) #TODO: choices
    controla_esfinteres = models.BooleanField(default=False)
    edad_controla_esfinteres = models.IntegerField(blank=True, null=True)
    usa_mamadera = models.BooleanField(default=False)
    es_alergico = models.BooleanField(default=False)
    toma_medicacion = models.BooleanField(default=False)
    en_tratamiento_medico = models.BooleanField(default=False)
    detalle_tratamiento = models.CharField(max_length=40, blank=True)
    tiene_convulsiones = models.BooleanField(default=False, help_text='en caso de temperatura')
    tiene_antitetanica = models.BooleanField(default=False)
    observaciones_medicas = models.TextField(blank=True, help_text='ingrese aqui informacion adicional de ser necesario')
    traslado_emergencia = models.CharField(max_length=40, blank=True) #TODO: choices
    telefono_emergencia = models.IntegerField(help_text='Ingresar sólo los números sin puntos', blank=True, null=True)

    #otros
    expresion_verbal = models.BooleanField(default=False)
    vocabulario = models.CharField(max_length=40, blank=True, help_text='como es su vocabulario y lenguaje')

    class Meta:
        ordering = ['fecha_ingreso',] #primero que se anoto FCFS
    
    # FILTER O GET ???
        #FIX get_deuda de alumno devuelve lista, de empleado int
    def get_deuda(self, extra=False):
        lista = []
        try: # FIX usar https://docs.djangoproject.com/en/1.3/ref/models/querysets/#get-or-create
            c = Cuota.objects.filter(alumno=self.id, paga=False)
            deuda_cuotas = sum([cuota.deuda for cuota in c ])
            u = UnicoPago.objects.filter(alumno=self.id, paga=False)
            deuda_unicos = sum([p_unico.deuda for p_unico in u ])
            lista.extend([deuda_cuotas, deuda_unicos])
            if extra:
                lista.extend([c,u])
            return lista

        except: return 0

    def get_informes(self, limit=5):
        return Informe.objects.filter(alumno=self.id)[:limit]

    def last_payments(self, limit=5):
        try: # FIX usar https://docs.djangoproject.com/en/1.3/ref/models/querysets/#get-or-create
            p = Pago.objects.filter(alumno=self.id)[:limit]
            return p
        except: return None

    def suscript_services(self):
        return ServicioSuscripto.objects.filter(alumno=self.id)

    def get_absolute_url(self):
        return reverse('alumnos-jardin')


class Sala(models.Model):
    sala = models.IntegerField(max_length=2, choices=SALA_CHOICES)
    turno = models.IntegerField(max_length=1, choices=TURNO_CHOICES)
    seccion = models.IntegerField(max_length=1, choices=SECCION_CHOICES)
    anio_lectivo = models.IntegerField(max_length=4)
    fecha_inicio = models.DateField(default=date.today)
    capacidad = models.IntegerField(max_length=2) #capacidad maxima de la sala


    def __unicode__(self):
        return u'Sala: %s, Turno: %s' % (self.get_sala_display(), self.get_turno_display())

    def get_alumnos(self):
        return self.alumno_set.all()

    def get_absolute_url(self):
        return reverse('salas-jardin')


class AlumnoSala(models.Model):
    alumno = models.ForeignKey(Alumno)
    sala = models.ForeignKey(Sala)
    estado = models.IntegerField(max_length=2, choices=ESTADO_ALUMNO_SALA_CHOICES)
    comentarios = models.TextField(blank=True)

    #class Meta:
    #    ordering = ['alumno.fecha_ingreso',] #primero que se anoto
    
    def __unicode__(self):
        return '%s: %s, %d' % (self.alumno.apellido, self.estado, self.sala.anio_lectivo)



class Maestra(Empleado):
    salas = models.ManyToManyField(Sala)

    def get_absolute_url(self):
        #return "/efinance/detalle_gasto/%d/" % self.id
        return reverse('maestras-jardin')


class Informe(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    alumno = models.ForeignKey(Alumno)
    maestra = models.ForeignKey(Maestra)
    fecha = models.DateField(default=date.today)

    class Meta:
        ordering = ['-fecha',]

    def __unicode__(self):
        return u'Informe de la maestra: %s para el alumno %s' % (self.maestra.get_full_name(), self.alumno.get_full_name())


