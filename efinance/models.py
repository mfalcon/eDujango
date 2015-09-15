# -*- encoding: utf-8 -*-

from django.db import models

#from finance.models import Persona

from efinance.tipos import *
from django.core.urlresolvers import reverse
from datetime import datetime
from datetime import date

import pdb

from finance.models import CustomUser
from tenant_schemas.models import TenantMixin



class Client(TenantMixin):
    nombre = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True




class Empleado(CustomUser):
    puesto = models.IntegerField(max_length=1, choices=PUESTO_CHOICES)

    def get_deuda(self):
        #pdb.set_trace()
        try:
            sueldos = Sueldo.objects.filter(empleado=self.id, pago=False)
            return sum([sueldo.deuda for sueldo in sueldos])
        except:
            return None

    def get_sueldo_bruto(self):
        #pdb.set_trace() #FIX ME!! El problema es que estoy creando un empleado y una maestra con diferentes id
        try:
            h = Honorarios.objects.get(empleado=self.id)
            l = [h.basico, h.obrasocial]
            if h.asig_por_hijo:
                l.append(h.asig_por_hijo)
            return sum(l)
        except:
            print 'Aun no ha creado honorarios para %s' % (self.get_full_name())

    def get_ultimos_pagos(self, limit=5):
        try:
            ult_pagos = PagoSueldo.objects.filter(empleado=self.id)[:limit]
            return ult_pagos
        except:
            return None

    def get_absolute_url(self):
        return reverse('empleados-jardin')

        
class Honorarios(models.Model):
    basico = models.DecimalField(max_digits=10, decimal_places=2)
    obrasocial = models.DecimalField('Obra Social', max_digits=10, decimal_places=2)
    asig_por_hijo = models.DecimalField('Asignacion por hijo', max_digits=10, decimal_places=2, blank=True, null=True)
    empleado = models.ForeignKey(Empleado, unique=True)

    class Meta:
        verbose_name = "Honorario"
        verbose_name_plural = "Honorarios"

    def __unicode__(self):
        return u'Honorarios empleado: %s' % (self.empleado.last_name)

    # TODO Analizar caso opcionales
    def get_sueldo_bruto(self):
        return sum([self.basico,self.obrasocial,self.asig_por_hijo])

    def get_sueldo_neto(self):
        pass

    def get_absolute_url(self):
        return reverse('honorarios-jardin')


class Honorarios2(models.Model):
    nominal = models.DecimalField(max_digits=10, decimal_places=2)
    antiguedad = models.DecimalField('Antiguedad', max_digits=10, decimal_places=2)
    bon_rem_doc = models.DecimalField('Bonificacion remunerativa docente', max_digits=10, decimal_places=2, null=True, blank=True)
    bon_ens = models.DecimalField('Bonificacion por ens.', max_digits=10, decimal_places=2, null=True, blank=True)
    bon_ant = models.DecimalField('Bonificacion por antiguedad', max_digits=10, decimal_places=2, null=True, blank=True)
    bon_rem_nobon = models.DecimalField('Bonificacion rem. no bonificable', max_digits=10, decimal_places=2, null=True, blank=True)
    bon_sin_ap = models.DecimalField('Bonificacion sin aporte', max_digits=10, decimal_places=2, null=True, blank=True)
    asig_res = models.DecimalField('Asignacion Res. 02/04', max_digits=10, decimal_places=2, null=True, blank=True)
    #redondeo = models.DecimalField('Bonificacion sin aporte', max_digits=10, decimal_places=2, blank=True)
    ips = models.DecimalField('IPS', max_digits=10, decimal_places=2, null=True, blank=True)
    obra_social = models.DecimalField('Obra Social', max_digits=10, decimal_places=2, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, unique=True)

    class Meta:
        verbose_name = "Honorario"
        verbose_name_plural = "Honorarios"

    def __unicode__(self):
        return u'Honorarios empleado: %s' % (self.empleado.last_name)


class Sueldo(models.Model): # importe, deuda = h.get_sueldo_bruto
    empleado = models.ForeignKey(Empleado)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    pago = models.BooleanField(default=False)
    deuda = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-fecha"]

    def __unicode__(self):
        return u'%s %s recibe %s correspondientes a %s' % (self.empleado.last_name, self.empleado.first_name, self.importe, self.fecha)

    def get_dinero_adeudado(self):
        pass

    def get_absolute_url(self):
        return reverse('sueldos-jardin')


class PagoSueldo(models.Model):
    empleado = models.ForeignKey(Empleado)
    abona = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=date.today)
    comentarios = models.TextField(blank=True)

    class Meta:
        verbose_name = "Pago de sueldo"
        verbose_name_plural = "Pago de sueldos"
        ordering = ["-fecha"]

    def __unicode__(self):
        return u'Se le han pagado %s pesos a %s el %s' % (self.abona, self.empleado.last_name, self.fecha)

    def get_absolute_url(self):
        return reverse('pagos-jardin')

        
class Gasto(models.Model):
    tipo = models.IntegerField(max_length=1, choices=GASTO_CHOICES)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=date.today)
    pago = models.BooleanField(default=False)
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __unicode__(self):
        return u'%s $%s' % (self.get_tipo_display(), self.importe)

    def get_tipo(self):
        return self.get_tipo_display()

    def get_absolute_url(self):
        #return "/efinance/detalle_gasto/%d/" % self.id
        return reverse('gastos-jardin')

    def is_pago(self):
        if self.pago: return u'Sí'
        return u'No'
