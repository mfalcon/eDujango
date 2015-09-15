from django.conf.urls import patterns,url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from efinance import views
 

urlpatterns = patterns('',  
    # finance employees
    url(r'^empleados/nuevo_pago/(?P<emp_id>\d+)/$', views.pagar_sueldo, name='f_pagar_sueldo'),
    url(r'^empleados/mod_pago/(?P<pago_id>\d+)/$', views.modificar_pago_sueldo, name='e_mod_pago_sueldo'),
    url(r'^empleados/$', views.empleados, name='f_empleados'),
    url(r'^empleados/gen_sueldos/$', views.sueldos_mensuales, name='f_sueldos_mensuales'),
    #url(r'^finance/students/new_payment/(?P<st_id>\d+)/$', views.new_payment, name='f_new_payment'),
    url(r'^einfo/(?P<emp_id>\d+)/$', views.f_empleado_info, name='f_empleado_info'),
        
    # finance gastos
    url(r'^gastos/$', views.gastos, name='f_gastos'),
    url(r'^nuevo_gasto/$', views.nuevo_gasto, name='f_nuevo_gasto'),
    url(r'^mod_gasto/(?P<gasto_id>\d+)$', views.modificar_gasto, name='e_modificar_gasto'),
    url(r'^detalle_gasto/(?P<gasto_id>\d+)/$', views.f_gasto_info, name='f_gasto_info'),
    
    #cashflow
    url(r'^cashflow_diario/$', views.f_cashflow_diario, name='f_cashflow_diario'),
    url(r'^cashflow_semanal/$', views.f_cashflow_semanal, name='f_cashflow_semanal'),
    url(r'^cashflow_mensual/$', views.f_cashflow_mensual, name='f_cashflow_mensual'),
    url(r'^cashflow_anual/$', views.f_cashflow_anual, name='f_cashflow_anual'),
    url(r'^estado_financiero/$', views.f_estado_financiero, name='f_estado_financiero'),

    
)

urlpatterns += patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name="finance/f_index.html")), name="f_index"),
    url(r'^cashflow/$', login_required(TemplateView.as_view(template_name="efinance/f_cashflow.html")), name="f_cashflow"),
)
