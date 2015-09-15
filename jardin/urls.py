# Importaciones Django
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


# Importaciones propias
from .views import *

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name="new/base.html"), name="jardin"),

	url(r'^alumnos/$', GestionAlumnosView.as_view(), name='alumnos-jardin'), 
	url(r'^alumnos/nuevo/$', AlumnoCreateView.as_view(), name='alumno-jardin-nuevo'), 
	url(r'^alumnos/(?P<pk>[0-9]+)/detalle/$', AlumnoDetailView.as_view(), name='alumno-jardin-detail'), 
	url(r'^alumnos/(?P<pk>[0-9]+)/editar/$', AlumnoUpdateView.as_view(), name='alumno-jardin-update'), 
	url(r'^alumnos/(\d+)/eliminar/$', 'jardin.views.alumnoDeleteView', name='alumno-jardin'),

	url(r'^responsables/$', GestionResponsableView.as_view(), name='responsables-jardin'), 
	url(r'^responsables/nuevo/$', ResponsableCreateView.as_view(), name='responsable-jardin-nuevo'), 
	url(r'^responsables/(?P<pk>[0-9]+)/detalle/$', ResponsableDetailView.as_view(), name='responsable-jardin-detail'), 
	url(r'^responsables/(?P<pk>[0-9]+)/editar/$', ResponsableUpdateView.as_view(), name='responsable-jardin-update'), 
	url(r'^responsables/(\d+)/eliminar/$', 'jardin.views.responsableDeleteView', name='responsable-jardin'),

	url(r'^autorizados/$', GestionAutorizadoView.as_view(), name='autorizados-jardin'), 
	url(r'^autorizados/nuevo/$', AutorizadoCreateView.as_view(), name='autorizado-jardin-nuevo'), 
	url(r'^autorizados/(?P<pk>[0-9]+)/detalle/$', AutorizadoDetailView.as_view(), name='autorizado-jardin-detail'), 
	url(r'^autorizados/(?P<pk>[0-9]+)/editar/$', AutorizadoUpdateView.as_view(), name='autorizado-jardin-update'), 
	url(r'^autorizados/(\d+)/eliminar/$', 'jardin.views.autorizadoDeleteView', name='autorizado-jardin'),

	url(r'^salas/$', GestionSalaView.as_view(), name='salas-jardin'), 
	url(r'^salas/nuevo/$', SalaCreateView.as_view(), name='sala-jardin-nuevo'), 
	url(r'^salas/(?P<pk>[0-9]+)/detalle/$', SalaDetailView.as_view(), name='sala-jardin-detail'), 
	url(r'^salas/(?P<pk>[0-9]+)/editar/$', SalaUpdateView.as_view(), name='sala-jardin-update'), 
	url(r'^salas/(\d+)/eliminar/$', 'jardin.views.salaDeleteView', name='sala-jardin'),

	url(r'^cuotas/$', GestionCuotaView.as_view(), name='cuotas-jardin'), 
	url(r'^cuotas/nuevo/$', CuotaCreateView.as_view(), name='cuota-jardin-nuevo'), 
	url(r'^cuotas/(?P<pk>[0-9]+)/detalle/$', CuotaDetailView.as_view(), name='cuota-jardin-detail'), 
	url(r'^cuotas/(?P<pk>[0-9]+)/editar/$', CuotaUpdateView.as_view(), name='cuota-jardin-update'), 
	url(r'^cuotas/(\d+)/eliminar/$', 'jardin.views.cuotaDeleteView', name='cuota-jardin'),

	url(r'^pagos/$', GestionPagoView.as_view(), name='pagos-al-jardin'), 
	url(r'^pagos/nuevo/$', PagoCreateView.as_view(), name='pago-al-jardin-nuevo'), 
	url(r'^pagos/(?P<pk>[0-9]+)/detalle/$', PagoDetailView.as_view(), name='pago-al-jardin-detail'), 
	url(r'^pagos/(?P<pk>[0-9]+)/editar/$', PagoUpdateView.as_view(), name='pago-al-jardin-update'), 
	url(r'^pagos/(\d+)/eliminar/$', 'jardin.views.pagoDeleteView', name='pago-al-jardin'),

	url(r'^pagos-unicos/$', GestionPagoUnicoView.as_view(), name='pagos-unicos-al-jardin'), 
	url(r'^pagos-unicos/nuevo/$', PagoUnicoCreateView.as_view(), name='pago-unicos-al-jardin-nuevo'), 
	url(r'^pagos-unicos/(?P<pk>[0-9]+)/detalle/$', PagoUnicoDetailView.as_view(), name='pago-unicos-al-jardin-detail'), 
	url(r'^pagos-unicos/(?P<pk>[0-9]+)/editar/$', PagoUnicoUpdateView.as_view(), name='pago-unicos-al-jardin-update'), 
	url(r'^pagos-unicos/(\d+)/eliminar/$', 'jardin.views.pagounicoDeleteView', name='pago-unicos-al-jardin'),

	url(r'^gestion-empleados/empleados/$', GestionEmpleadoView.as_view(), name='empleados-jardin'), 
	url(r'^gestion-empleados/empleados/nuevo/$', EmpleadoCreateView.as_view(), name='empleado-jardin-nuevo'), 
	url(r'^gestion-empleados/empleados/(?P<pk>[0-9]+)/detalle/$', EmpleadoDetailView.as_view(), name='empleado-jardin-detail'), 
	url(r'^gestion-empleados/empleados/(?P<pk>[0-9]+)/editar/$', EmpleadoUpdateView.as_view(), name='empleado-jardin-update'), 
	url(r'^gestion-empleados/empleados/(\d+)/eliminar/$', 'jardin.views.empleadoDeleteView', name='empleado-jardin'),

	url(r'^gestion-empleados/maestras/$', GestionMaestraView.as_view(), name='maestras-jardin'), 
	url(r'^gestion-empleados/maestras/nuevo/$', MaestraCreateView.as_view(), name='maestra-jardin-nuevo'), 
	url(r'^gestion-empleados/maestras/(?P<pk>[0-9]+)/detalle/$', MaestraDetailView.as_view(), name='maestra-jardin-detail'), 
	url(r'^gestion-empleados/maestras/(?P<pk>[0-9]+)/editar/$', MaestraUpdateView.as_view(), name='maestra-jardin-update'), 
	url(r'^gestion-empleados/maestras/(\d+)/eliminar/$', 'jardin.views.maestraDeleteView', name='maestra-jardin'),

	url(r'^gestion-empleados/honorarios/$', GestionHonorarioView.as_view(), name='honorarios-jardin'), 
	url(r'^gestion-empleados/honorarios/nuevo/$', HonorarioCreateView.as_view(), name='honorario-jardin-nuevo'), 
	url(r'^gestion-empleados/honorarios/(?P<pk>[0-9]+)/detalle/$', HonorarioDetailView.as_view(), name='honorario-jardin-detail'), 
	url(r'^gestion-empleados/honorarios/(?P<pk>[0-9]+)/editar/$', HonorarioUpdateView.as_view(), name='honorario-jardin-update'), 
	url(r'^gestion-empleados/honorarios/(\d+)/eliminar/$', 'jardin.views.honorarioDeleteView', name='honorario-jardin'),

	url(r'^gestion-empleados/sueldos/$', GestionSueldoView.as_view(), name='sueldos-jardin'), 
	url(r'^gestion-empleados/sueldos/nuevo/$', SueldoCreateView.as_view(), name='sueldo-jardin-nuevo'), 
	url(r'^gestion-empleados/sueldos/(?P<pk>[0-9]+)/detalle/$', SueldoDetailView.as_view(), name='sueldo-jardin-detail'), 
	url(r'^gestion-empleados/sueldos/(?P<pk>[0-9]+)/editar/$', SueldoUpdateView.as_view(), name='sueldo-jardin-update'), 
	url(r'^gestion-empleados/sueldos/(\d+)/eliminar/$', 'jardin.views.sueldoDeleteView', name='sueldo-jardin'),

	url(r'^gestion-empleados/pagos/$', GestionPagoSueldoView.as_view(), name='pagos-jardin'), 
	url(r'^gestion-empleados/pagos/nuevo/$', PagoSueldoCreateView.as_view(), name='pago-jardin-nuevo'), 
	url(r'^gestion-empleados/pagos/(?P<pk>[0-9]+)/detalle/$', PagoSueldoDetailView.as_view(), name='pago-jardin-detail'), 
	url(r'^gestion-empleados/pagos/(?P<pk>[0-9]+)/editar/$', PagoSueldoUpdateView.as_view(), name='pago-jardin-update'), 
	url(r'^gestion-empleados/pagos/(\d+)/eliminar/$', 'jardin.views.pagosueldoDeleteView', name='pago-jardin'),

	url(r'^gestion-alumnos/tipos-servicios/$', GestionTipoServicioView.as_view(), name='tipo-servicios-jardin'), 
	url(r'^gestion-alumnos/tipos-servicios/nuevo/$', TipoServicioCreateView.as_view(), name='tipo-servicio-jardin-nuevo'), 
	url(r'^gestion-alumnos/tipos-servicios/(?P<pk>[0-9]+)/detalle/$', TipoServicioDetailView.as_view(), name='tipo-servicio-jardin-detail'), 
	url(r'^gestion-alumnos/tipos-servicios/(?P<pk>[0-9]+)/editar/$', TipoServicioUpdateView.as_view(), name='tipo-servicio-jardin-update'), 
	url(r'^gestion-alumnos/tipos-servicios/(\d+)/eliminar/$', 'jardin.views.tiposervicioDeleteView', name='tipo-servicio-jardin'),

	url(r'^gestion-alumnos/servicios/$', GestionServicioSuscriptoView.as_view(), name='servicios-jardin'), 
	url(r'^gestion-alumnos/servicios/nuevo/$', ServicioSuscriptoCreateView.as_view(), name='servicio-jardin-nuevo'), 
	url(r'^gestion-alumnos/servicios/(?P<pk>[0-9]+)/detalle/$', ServicioSuscriptoDetailView.as_view(), name='servicio-jardin-detail'), 
	url(r'^gestion-alumnos/servicios/(?P<pk>[0-9]+)/editar/$', ServicioSuscriptoUpdateView.as_view(), name='servicio-jardin-update'), 
	url(r'^gestion-alumnos/servicios/(\d+)/eliminar/$', 'jardin.views.serviciosuscriptoDeleteView', name='servicio-jardin'),

	url(r'^gestion-alumnos/tipos-unicos-pagos/$', GestionTipoUnicoPagoView.as_view(), name='tipos-unicos-pagos-jardin'), 
	url(r'^gestion-alumnos/tipos-unicos-pagos/nuevo/$', TipoUnicoPagoCreateView.as_view(), name='tipo-unico-pago-jardin-nuevo'), 
	url(r'^gestion-alumnos/tipos-unicos-pagos/(?P<pk>[0-9]+)/detalle/$', TipoUnicoPagoDetailView.as_view(), name='tipo-unico-pago-jardin-detail'), 
	url(r'^gestion-alumnos/tipos-unicos-pagos/(?P<pk>[0-9]+)/editar/$', TipoUnicoPagoUpdateView.as_view(), name='tipo-unico-pago-jardin-update'), 
	url(r'^gestion-alumnos/tipos-unicos-pagos/(\d+)/eliminar/$', 'jardin.views.tipounicopagoDeleteView', name='tipo-unico-pago-jardin'),

	url(r'^gestion-finanzas/gastos/$', GestionGastoView.as_view(), name='gastos-jardin'), 
	url(r'^gestion-finanzas/gastos/nuevo/$', GastoCreateView.as_view(), name='gasto-jardin-nuevo'), 
	url(r'^gestion-finanzas/gastos/(?P<pk>[0-9]+)/detalle/$', GastoDetailView.as_view(), name='gasto-jardin-detail'), 
	url(r'^gestion-finanzas/gastos/(?P<pk>[0-9]+)/editar/$', GastoUpdateView.as_view(), name='gasto-jardin-update'), 
	url(r'^gestion-finanzas/gastos/(\d+)/eliminar/$', 'jardin.views.gastoDeleteView', name='gasto-jardin'),


	url(r'^insertar_arancel/$', insertar_arancel, name='insertar_arancel'),
	url(r'^cambiar_division/$', cambiar_division, name='cambiar_division'),



)
