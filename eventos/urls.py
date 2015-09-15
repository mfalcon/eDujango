from django.conf.urls import patterns,url
from eventos import views
 

urlpatterns = patterns('',
    url(r'^$', views.noticias, name='noti_index'),
    url(r'^nueva_noticia/$', views.nueva_noticia, name='nueva_noti'),
    url(r'^modificar_noticia/(?P<noti_id>\d+)/$', views.modificar_noticia, name='modificar_noticia'),
    url(r'^mod_noticia/$', views.mod_not, name='mod_not'),
)
