# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import UserManager

from finance.tipos import *

from datetime import datetime
from datetime import date



class Persona(models.Model):
    apellido = models.CharField(max_length=30)
    nombre1 = models.CharField('Primer nombre', max_length=30, blank=True)
    nombre2 = models.CharField('Segundo nombre', max_length=30, blank=True)
    tipo_doc = models.IntegerField('Tipo documento', max_length=1, choices=DOC_CHOICES, default=DNI, blank=True)
    num_doc = models.IntegerField('Número documento', max_length=8,
                                  help_text='Ingresar sólo los números sin puntos', blank=True, null=True) # En el admin pedir solo numeros sin puntos
    sexo = models.IntegerField(max_length=1, choices=SEXO_CHOICES, default=0)
    fecha_nac = models.DateField('Fecha de nacimiento', blank=True, null=True)
    domicilio = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=20, blank=True)
    telefono = models.IntegerField(help_text='Ingresar sólo los números sin puntos', blank=True, null=True)    # En el admin pedir que se ingrese solo numero
    email = models.EmailField(blank=True)
    nacionalidad = models.IntegerField(max_length=2, choices=NAC_CHOICES, default=AR, blank=True)

    class Meta:
        abstract = True
        ordering = ['apellido',]

    def __unicode__(self):
        return u'%s %s' % (self.apellido, self.nombre1)

    def get_full_name(self):
        nombre = self.apellido + ', ' + self.nombre1
        if self.nombre2:
            nombre += ' ' + self.nombre2
        return nombre
        

class UserManager(BaseUserManager):
    def _create_user(self, num_doc, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given num_doc and password.
        """
        now = timezone.now()
        if not num_doc:
            raise ValueError('Se debe setear un número de documento')
        user = self.model(num_doc=num_doc,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, num_doc, password=None, **extra_fields):
        return self._create_user(num_doc, password, False, False,
                                 **extra_fields)
 
    def create_superuser(self, num_doc, password, **extra_fields):
        u = self.create_user(num_doc, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class CustomUser(AbstractBaseUser, PermissionsMixin):
    tipo_doc = models.IntegerField('Tipo documento', max_length=1, choices=DOC_CHOICES, default=DNI, blank=True)
    num_doc = models.IntegerField('numero documento', max_length=8,
                                  help_text='Ingresar sólo los números sin puntos', unique=True) # En el admin pedir solo numeros sin puntos
    email = models.EmailField('email', blank=True, null=True)
    first_name = models.CharField(_('nombre'), max_length=30)
    second_name = models.CharField(_('segundo nombre'), max_length=30, blank=True)
    last_name = models.CharField(_('apellido'), max_length=30)
    
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_email_verified = models.BooleanField('verified', default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    
    sexo = models.IntegerField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    fecha_nac = models.DateField('Fecha de nacimiento', blank=True, null=True)
    domicilio = models.CharField(max_length=50, blank=True, null=True)
    localidad = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.IntegerField(help_text='Ingresar sólo los números sin puntos', blank=True, null=True)    # En el admin pedir que se ingrese solo numero
    nacionalidad = models.IntegerField(max_length=2, choices=NAC_CHOICES, default=AR, blank=True)
 
    USERNAME_FIELD = 'num_doc'
 
    objects = UserManager()
 
    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
      return u' '.join((self.first_name, self.second_name ,self.last_name))
    
    def get_short_name():
      return self.first_name

    def get_tipo(self):
        if hasattr(self, 'profesor'):
            return 'Profesor'
        elif hasattr(self, 'alumnocolegio'):
            return 'Alumno'
        else:
            return 'No se'


class Responsable(CustomUser):
    relacion = models.IntegerField(max_length=1, choices=REL_CHOICES, default=MADRE)
    ocupacion = models.CharField(max_length=30)
    telefono_laboral1 = models.IntegerField(help_text='Ingresar sólo los números sin puntos', blank=True, null=True)
    telefono_laboral2 = models.IntegerField(help_text='Ingresar sólo los números sin puntos', blank=True, null=True)
    como_conocio = models.IntegerField(help_text='Como conoció al jardín?', max_length=2, choices=CONOCIO_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Responsables'

    def get_absolute_url(self):
        return reverse('responsables-jardin')

   

class Autorizado(CustomUser):
    relacion = models.IntegerField(max_length=1, choices=REL_CHOICES, default=MADRE)
    otra = models.CharField(max_length=40, blank=True)

    def get_absolute_url(self):
        return reverse('autorizados')


class Cuota(models.Model):
    alumno = models.ForeignKey('students.Alumno')
    importe = models.DecimalField(max_digits=10, decimal_places=2) #TODO: inicial, intereses punitorios
    deuda = models.DecimalField(max_digits=10, decimal_places=2) # al principio = a importe, si es 0 => paga=True
    fecha = models.DateField()
    paga = models.BooleanField(default=False)
    concepto = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["-fecha"]  #primer elemento de la lista, ultima fecha

    def __unicode__(self):
        #fecha = self.fecha.month, self.fecha.year
        return u'%s %s paga %s correspondientes a %s' % (self.alumno.apellido, self.alumno.nombre1, self.importe, self.fecha)

    def get_absolute_url(self):
        return reverse('cuotas-jardin')



class Pago(models.Model):
    #pago que se realiza, no diferencia entre cuotas y pagos unicos
    alumno = models.ForeignKey('students.Alumno')
    responsable = models.ForeignKey('Responsable')
    #tipo_comprobante = models.IntegerField(max_length=1, choices=COMP_CHOICES, default=RECIBO)
    abona = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=date.today)
    comentarios = models.TextField(blank=True)


    class Meta:
       ordering = ["-fecha"]

    def __unicode__(self):
        return u'%s %s ha pagado %s el %s' % (self.alumno.apellido, self.alumno.nombre1, self.abona, self.fecha)


class ItemPago(models.Model):
    pago = models.ForeignKey(Pago)
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%s' % self.descripcion


class ServicioSuscripto(models.Model):
    alumno = models.ForeignKey('students.Alumno')
    tipo = models.ForeignKey('TipoServicio')
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    class Meta:
        verbose_name = "Servicio Suscripto"
        verbose_name_plural = "Servicios Suscriptos"

    def __unicode__(self):
        return u' %s paga %s por el servicio: %s' % (self.alumno, self.importe, self.tipo)

    def save(self, **kwargs):
        if not self.importe:
            self.importe = int(self.tipo.importe)
        super(ServicioSuscripto, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('servicios-jardin')


class TipoServicio(models.Model):
    tipo = models.IntegerField(max_length=1, choices=TIPO_CHOICES, default=CUOTA_BASE)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Tipo Servicio"
        verbose_name_plural = "Tipos de servicio"

    def __unicode__(self):
        return '%s' % (self.get_tipo_display())

    def get_absolute_url(self):
        return reverse('tipo-servicios-jardin')


class UnicoPago(models.Model):
    fecha = models.DateField(default=date.today)
    paga = models.BooleanField(default=False)
    responsable = models.ForeignKey('Responsable')
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #TODO: check if blank is a good practice
    alumno = models.ForeignKey('students.Alumno')
    tipo = models.ForeignKey('TipoUnicoPago')
    comentarios = models.TextField(blank=True)
    deuda = models.DecimalField(max_digits=10, decimal_places=2) #, blank=True) # al principio = a importe, si es 0 => paga=True

    class Meta:
        verbose_name = "Pago único"
        verbose_name_plural = "Pagos únicos"
        ordering = ["-fecha"]  #primer elemento de la lista, ultima fecha

    def __unicode__(self):
        return 'Se abonan %s por un/a %s' % (self.importe, self.tipo.get_tipo_display())

    def get_absolute_url(self):
        return reverse('pagos-unicos-al-jardin')
        
    #def save(self, **kwargs):
        #if not self.importe:
            #self.importe = int(self.tipo.importe)
        #self.deuda = self.importe
        #super(UnicoPago, self).save(**kwargs)


class TipoUnicoPago(models.Model):
    tipo = models.IntegerField(max_length=1, choices=ELEMENTO_CHOICES)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Tipo de pago único"
        verbose_name_plural = "Tipos de pago único"

    def __unicode__(self):
        return '%s' % (self.get_tipo_display())

    def get_absolute_url(self):
        return reverse('tipos-unicos-pagos-jardin')