from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


#from efinance.views import DemoView
#from efinance.views import empleados, f_cashflow_mensual, f_cashflow_diario, f_cashflow_semanal, f_cashflow_anual
#from finance.views import students

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^cashflow/$', 'direct_to_template', {'template': 'efinance/f_cashflow.html',
        #'extra_context': {} }, name='admin_f_cashflow'),
    #url(r'^admin/cashflow_diario/$', f_cashflow_diario, name='admin_cashflow_diario'),
    #url(r'^admin/cashflow_semanal/$', f_cashflow_semanal, name='admin_cashflow_semanal'),
    #url(r'^admin/cashflow_mensual/$', f_cashflow_mensual, name='admin_cashflow_mensual'),
    #url(r'^admin/cashflow_anual/$', f_cashflow_anual, name='admin_cashflow_anual'),
    #url(r'^admin/alumnos/$', students, name='admin_f_students'),
    #url(r'^admin/empleados/$', empleados, name='admin_f_empleados'),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^students/', include('students.urls')),
    (r'^finance/', include('finance.urls')),
    (r'^efinance/', include('efinance.urls')),
    (r'^eventos/', include('eventos.urls')),
    
    #blog
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    #url(r'^demo/$', DemoView.as_view(), name='demo'),

    url(r'^colegio/', include('college.urls')),
    url(r'^jardin/', include('jardin.urls')),

)
urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name="website/index.html"), name="home"),
    url(r'^app/$', login_required(TemplateView.as_view(template_name="index.html")), name="index"),
    url(r'^institucional/$', TemplateView.as_view(template_name="website/institucional.html"), name="institucional"),
    url(r'^actividades/$', TemplateView.as_view(template_name="website/actividades.html"), name="actividades"),
    url(r'^fotos/$', TemplateView.as_view(template_name="website/fotos.html"), name="fotos"),
    url(r'^salas/$', TemplateView.as_view(template_name="website/salas.html"), name="salas"),
    url(r'^contacto/$', TemplateView.as_view(template_name="website/contacto.html"), name="contacto"),

    url(r'^schedule/', include('schedule.urls')),
)  
