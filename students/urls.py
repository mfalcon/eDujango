from django.conf.urls import patterns,url
from django.views.generic import TemplateView
from students import views
 

urlpatterns = patterns('',
    url(r'^listado/$', views.students_list, name='st_students_list'),
    url(r'^nuevo/$', views.new_student, name='st_new_student'),
    url(r'^info/(?P<st_id>\d+)/$', views.student_info, name='st_student_info'),
    url(r'^personal/(?P<st_id>\d+)/$', views.student_personal_info, name='st_student_personal_info'),
    url(r'^informes/(?P<st_id>\d+)/$', views.student_reports, name='st_student_reports'),
    url(r'^informe/(?P<inf_id>\d+)/$', views.student_report, name='st_student_report'),
    url(r'^informe_pdf/(?P<inf_id>\d+)/$', views.get_informe_as_pdf, name='st_get_informe_as_pdf'), 
    url(r'^salas/$', views.salas, name='st_salas'),
    url(r'^info_sala/(?P<sala_id>\d+)/$', views.info_sala, name='st_info_sala'),
    url(r'^informes/nuevo/(?P<st_id>\d+)/$', views.nuevo_informe, name='st_nuevo_informe'),
    url(r'^informes/modificar/(?P<inf_id>\d+)/$', views.modificar_informe, name='st_modificar_informe'),
    url(r'^get_hermano_info/$', views.get_hermano_info, name='get_hermano_info'),

)

urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name="students/st_index.html"), name="st_index"),
)
