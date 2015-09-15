# coding: utf-8

# Importaciones Django
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db import models

# Importaciones Propias
from finance.models import CustomUser


	
class AlumnoColegio(CustomUser):
	division = models.ForeignKey('Division', related_name="alumnos")
	
	def get_absolute_url(self):
		return reverse('alumnos')


class Profesor(CustomUser):
	materias = models.ManyToManyField('MateriaDivision')

	def get_absolute_url(self):
		return reverse('profesores')

	def get_divisiones(self):
		divisiones = []
		for materia in self.materias.all():
			divisiones.append(materia.division)
		return divisiones

	def get_alumnos(self):
		div_prof = self.profesor.get_divisiones()
		return AlumnoColegio.objects.filter(division__in=div_prof)

	def get_nombre_materias(self):
		return [materia.materia.nombre for materia in self.materias.all()]


class Materia(models.Model):
	nombre = models.CharField(max_length=50)
	
	def __unicode__(self):
		return unicode(self.nombre)

	def get_absolute_url(self):
		return reverse('materias')


class MateriaDivision(models.Model):
	materia = models.ForeignKey('Materia')
	division = models.ForeignKey('Division')
	horario = models.TimeField()

	def __unicode__(self):
		return u'%s - %s - %s' % (self.materia, self.division, self.horario)

	def get_absolute_url(self):
		return reverse('materiasdivisiones')


class Division(models.Model):
	nivel = models.CharField(max_length=5)
	materias = models.ManyToManyField('Materia', through='MateriaDivision')

	def __unicode__(self):
		return unicode(self.nivel)

	def get_absolute_url(self):
		return reverse('divisiones')


class Asistencia(models.Model):
	alumno = models.ForeignKey('AlumnoColegio')
	fecha = models.DateField()
	estado = models.ForeignKey('EstadoAsistencia')

	def __unicode__(self):
		return unicode(self.alumno) + " " + unicode(self.fecha) + " " + unicode(self.estado)


class EstadoAsistencia(models.Model):
	nombre = models.CharField(max_length=50, unique=True)
	codigo = models.CharField(max_length=5, unique=True)

	def __unicode__(self):
		return unicode(self.nombre)
		

class Calificacion(models.Model):
	alumno = models.ForeignKey('AlumnoColegio', related_name='calificaciones')
	materia = models.ForeignKey('Materia')
	nota = models.DecimalField(max_digits=4,decimal_places=2,default='01.00')
	nota2 = models.CharField(max_length=10, null=True, blank=True)
	observacion = models.CharField(max_length=50, null=True, blank=True)
	fecha = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s - %s - %s' % (self.alumno, self.materia, self.nota)

	def get_absolute_url(self):
		return reverse('calificaciones')












@receiver(post_save, sender=Profesor)
def permisos_profesores(sender, **kwargs):
	try:
		if kwargs.get('created'):
			grupo = Group.objects.get(name='Profesores')
			profesor = kwargs.get('instance')
			profesor.groups.add(grupo)
	except Exception, e:
		print e

