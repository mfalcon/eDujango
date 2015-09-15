# Importaciones Django
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


# Importaciones propias
from .views import GestionProfesoresView, ProfesorCreateView, ProfesorDetailView, ProfesorUpdateView
from .views import GestionAlumnoColegioView, AlumnoColegioCreateView, AlumnoColegioDetailView, AlumnoColegioUpdateView
from .views import GestionMateriaView, MateriaCreateView, MateriaDetailView, MateriaUpdateView 
from .views import GestionDivisionView, DivisionCreateView, DivisionDetailView, DivisionUpdateView
from .views import GestionCalificacionView, CalificacionCreateView, CalificacionDetailView, CalificacionUpdateView
from .views import GestionMateriaDivisionView, MateriaDivisionCreateView, MateriaDivisionDetailView, MateriaDivisionUpdateView


urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name="new/base_colegio.html"), name="college"),

	url(r'^profesores/$', GestionProfesoresView.as_view(), name='profesores'), 
	url(r'^profesores/nuevo/$', ProfesorCreateView.as_view(), name='profesor-nuevo'), 
	url(r'^profesores/(?P<pk>[0-9]+)/detalle/$', ProfesorDetailView.as_view(), name='profesor-detail'), 
	url(r'^profesores/(?P<pk>[0-9]+)/editar/$', ProfesorUpdateView.as_view(), name='profesor-update'), 
	url(r'^profesores/(\d+)/eliminar/$', 'college.views.profesorDeleteView', name='profesorDeleteView'),

	url(r'^alumnos/$', GestionAlumnoColegioView.as_view(), name='alumnos'), 
	url(r'^alumnos/nuevo/$', AlumnoColegioCreateView.as_view(), name='alumno-nuevo'), 
	url(r'^alumnos/(?P<pk>[0-9]+)/detalle/$', AlumnoColegioDetailView.as_view(), name='alumno-detail'), 
	url(r'^alumnos/(?P<pk>[0-9]+)/editar/$', AlumnoColegioUpdateView.as_view(), name='alumno-update'), 
	url(r'^alumnos/(\d+)/eliminar/$', 'college.views.alumnoColegioDeleteView', name='alumno'),

	url(r'^materias/$', GestionMateriaView.as_view(), name='materias'), 
	url(r'^materias/nuevo/$', MateriaCreateView.as_view(), name='materia-nuevo'), 
	url(r'^materias/(?P<pk>[0-9]+)/detalle/$', MateriaDetailView.as_view(), name='materia-detail'), 
	url(r'^materias/(?P<pk>[0-9]+)/editar/$', MateriaUpdateView.as_view(), name='materia-update'), 
	url(r'^materias/(\d+)/eliminar/$', 'college.views.materiaDeleteView', name='materia'),

	url(r'^materiaDivision/$', GestionMateriaDivisionView.as_view(), name='materiasdivisiones'), 
	url(r'^materiaDivision/nuevo/$', MateriaDivisionCreateView.as_view(), name='materiadivision-nuevo'), 
	url(r'^materiaDivision/(?P<pk>[0-9]+)/detalle/$', MateriaDivisionDetailView.as_view(), name='materiadivision-detail'), 
	url(r'^materiaDivision/(?P<pk>[0-9]+)/editar/$', MateriaDivisionUpdateView.as_view(), name='materiadivision-update'), 
	url(r'^materiaDivision/(\d+)/eliminar/$', 'college.views.materiaDivisionDeleteView', name='materiadivision'),

	url(r'^divisiones/$', GestionDivisionView.as_view(), name='divisiones'), 
	url(r'^divisiones/nuevo/$', DivisionCreateView.as_view(), name='division-nuevo'), 
	url(r'^divisiones/(?P<pk>[0-9]+)/detalle/$', DivisionDetailView.as_view(), name='division-detail'), 
	url(r'^divisiones/(?P<pk>[0-9]+)/editar/$', DivisionUpdateView.as_view(), name='division-update'), 
	url(r'^divisiones/(\d+)/eliminar/$', 'college.views.divisionDeleteView', name='division'),

	url(r'^calificaciones/$', GestionCalificacionView.as_view(), name='calificaciones'), 
	url(r'^calificaciones/nuevo/$', CalificacionCreateView.as_view(), name='calificacion-nuevo'), 
	url(r'^calificaciones/(?P<pk>[0-9]+)/detalle/$', CalificacionDetailView.as_view(), name='calificacion-detail'), 
	url(r'^calificaciones/(?P<pk>[0-9]+)/editar/$', CalificacionUpdateView.as_view(), name='calificacion-update'), 
	url(r'^calificaciones/(\d+)/eliminar/$', 'college.views.calificacionDeleteView', name='calificacion'),
)
