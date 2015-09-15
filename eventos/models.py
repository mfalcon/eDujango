from django.db import models

from efinance.models import Empleado

from datetime import datetime, date

class Noticia2(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    texto = models.TextField()
    creador = models.ForeignKey(Empleado)
    fecha = models.DateField(default=date.today)
    
    class Meta:
        ordering = ['-fecha',]
    
    def __unicode__(self):
        return u'%s - %s' % (self.titulo, self.fecha)
