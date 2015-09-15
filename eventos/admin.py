from django.contrib import admin
from eventos.models import Noticia2

class Noticia2Admin(admin.ModelAdmin):
    list_display = ('titulo', 'creador', 'fecha')

admin.site.register(Noticia2, Noticia2Admin)



