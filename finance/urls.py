from django.conf.urls import patterns,url
from django.views.generic import TemplateView
from finance import views


urlpatterns = patterns('',
    # finance students
    url(r'^students/$', views.students, name='f_students'),
    url(r'^students/gen_payment/$', views.monthly_payments, name='f_monthly_payment'),
    url(r'^students/new_payment/(?P<st_id>\d+)/$', views.new_payment, name='f_new_payment'),
    url(r'^students/mod_pago/(?P<pago_id>\d+)/$', views.modificar_pago, name='f_mod_pago'),
    #url(r'^students/pdf_success/(?P<st_id>\d+)/$', views.pdf_success, name='f_pdf_success'),
    url(r'^students/new_unique_payment/(?P<st_id>\d+)/$', views.new_unique_payment, name='f_new_unique'),
    url(r'^ainfo/(?P<st_id>\d+)/$', views.f_student_info, name='f_student_info'),
    url(r'^reports/(?P<pago_id>\d+)/$', views.f_student_report, name='f_student_report'),

    url(r'^reports-nuevo/(?P<pago_id>\d+)/$', views.ReportPDFView.as_view(), name='f_student_report_nuevo'),

)

urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name="finance/f_index.html"), name="f_index"),
)
