# coding: utf-8

# Importaciones Django
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson

# Importaciones Propias
from core.mixins import LoginRequiredMixin
from .models import Profesor, AlumnoColegio, Materia, Division, MateriaDivision, Calificacion
from .forms import AlumnoColegioCrispyForm, ProfesorCrispyForm


class GestionProfesoresView(LoginRequiredMixin, ListView):

    
    paginate_by = 20

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''
        print self.request.user

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            profesores = Profesor.objects.all()

            q = Q(last_name__icontains=term_list[0]) | Q(first_name__icontains=term_list[0]) | Q(domicilio__icontains=term_list[0]) | Q(localidad__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(last_name__icontains=term) | Q(first_name__icontains=term) | Q(domicilio__icontains=term) | Q(localidad__icontains=term)), q.connector)

            return profesores.filter(q)
        else:
            return Profesor.objects.all()


class ProfesorCreateView(LoginRequiredMixin, CreateView):

    model = Profesor
    form_class = ProfesorCrispyForm
    fields = ['password', 'groups', 'tipo_doc', 'num_doc', 'email', 'first_name', 'second_name',
              'last_name', 'sexo', 'fecha_nac', 'domicilio', 'localidad', 'telefono', 
              'nacionalidad', 'materias']

    @method_decorator(permission_required('college.add_profesor'))
    def dispatch(self, *args, **kwargs):
        return super(ProfesorCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(ProfesorCreateView, self).form_valid(form)


class ProfesorDetailView(LoginRequiredMixin, DetailView):

    model = Profesor


class ProfesorUpdateView(LoginRequiredMixin, UpdateView):

    model = Profesor
    form_class = ProfesorCrispyForm
    fields = ['password', 'groups', 'tipo_doc', 'num_doc', 'email', 'first_name', 'second_name',
              'last_name', 'sexo', 'fecha_nac', 'domicilio', 'localidad', 'telefono', 
              'nacionalidad', 'materias']

    template_name = "college/profesor_update_form.html"

    @method_decorator(permission_required('college.change_profesor'))
    def dispatch(self, *args, **kwargs):
        return super(ProfesorUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(ProfesorUpdateView, self).form_valid(form)
    

def profesorDeleteView(request, id):
    profesor = Profesor.objects.get(pk=id)
    profesor.delete()
    return HttpResponseRedirect(reverse('profesores'))


class GestionAlumnoColegioView(LoginRequiredMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''

        user = self.request.user
        if user.get_tipo() == 'Profesor': # Si es profesor sólo ve sus alumnos
            alumnos = user.profesor.get_alumnos()
        else:
            alumnos = AlumnoColegio.objects.all()

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            q = Q(last_name__icontains=term_list[0]) | Q(first_name__icontains=term_list[0]) | Q(domicilio__icontains=term_list[0]) | Q(localidad__icontains=term_list[0]) | Q(sexo__icontains=term_list[0])  
            for term in term_list[1:]:
                q.add((Q(last_name__icontains=term) | Q(first_name__icontains=term) | Q(domicilio__icontains=term) | Q(localidad__icontains=term) | Q(sexo__icontains=term)), q.connector)

            return alumnos.filter(q)
        else:
            return alumnos


class AlumnoColegioCreateView(LoginRequiredMixin, CreateView):

    model = AlumnoColegio
    form_class = AlumnoColegioCrispyForm
    fields = ['password','tipo_doc', 'num_doc', 'email', 'first_name', 'second_name',
              'last_name', 'sexo', 'fecha_nac', 'domicilio', 'localidad', 'telefono', 
              'nacionalidad', 'division']

    @method_decorator(permission_required('college.add_alumnocolegio'))
    def dispatch(self, *args, **kwargs):
        return super(AlumnoColegioCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(AlumnoColegioCreateView, self).form_valid(form)


class AlumnoColegioDetailView(LoginRequiredMixin, DetailView):

    model = AlumnoColegio
    

class AlumnoColegioUpdateView(LoginRequiredMixin, UpdateView):

    model = AlumnoColegio
    form_class = AlumnoColegioCrispyForm
    fields = ['password','tipo_doc', 'num_doc', 'email', 'first_name', 'second_name',
              'last_name', 'sexo', 'fecha_nac', 'domicilio', 'localidad', 'telefono', 
              'nacionalidad', 'division']
              
    template_name = "college/alumno_update_form.html"

    @method_decorator(permission_required('college.change_alumnocolegio'))
    def dispatch(self, *args, **kwargs):
        return super(AlumnoColegioUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(AlumnoColegioUpdateView, self).form_valid(form)
    

def alumnoColegioDeleteView(request, id):
    alumno = AlumnoColegio.objects.get(pk=id)
    alumno.delete()
    return HttpResponseRedirect(reverse('alumnos'))


class GestionMateriaView(LoginRequiredMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''

        user = self.request.user
        tipo_usuario = user.get_tipo()
        if tipo_usuario == 'Profesor':
            materias_prof = user.profesor.get_nombre_materias
            materias = Materia.objects.filter(nombre__in=materias_prof)
        elif tipo_usuario == 'Alumno':
            materias = user.alumnocolegio.division.materias.all()
        else:
            materias = Materia.objects.all()

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            q = Q(nombre__icontains=term_list[0]) 
            for term in term_list[1:]:
                q.add((Q(nombre__icontains=term)), q.connector)

            return materias.filter(q)
        else:
            return materias


class MateriaCreateView(LoginRequiredMixin, CreateView):

    model = Materia
    #fields = ['nombre','apellido','direccion','ciudad','telefono','celular']

    @method_decorator(permission_required('college.add_materia'))
    def dispatch(self, *args, **kwargs):
        return super(MateriaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(MateriaCreateView, self).form_valid(form)


class MateriaDetailView(LoginRequiredMixin, DetailView):

    model = Materia


class MateriaUpdateView(LoginRequiredMixin, UpdateView):

    model = Materia
    #fields = ['nombre','apellido','direccion','ciudad','telefono','celular']
    template_name = "college/materia_update_form.html"

    @method_decorator(permission_required('college.change_materia'))
    def dispatch(self, *args, **kwargs):
        return super(MateriaUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(MateriaUpdateView, self).form_valid(form)
    

def materiaDeleteView(request, id):
    materia = Materia.objects.get(pk=id)
    materia.delete()
    return HttpResponseRedirect(reverse('materias'))


class GestionDivisionView(LoginRequiredMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''

        user = self.request.user

        if user.get_tipo() == 'Profesor': # Si es profesor solo ve sus divisiones
            div_profesor = user.profesor.get_divisiones()
            divisiones = Division.objects.filter(nivel__in=div_profesor)
        else:
            divisiones = Division.objects.all()

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            q = Q(nivel__icontains=term_list[0]) | Q(nivel__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(materia__icontains=term) | Q(nivel__icontains=term)), q.connector)

            return divisiones.filter(q)
        else:
            return divisiones


class DivisionCreateView(LoginRequiredMixin, CreateView):

    model = Division
    #fields = ['nombre','apellido','direccion','ciudad','telefono','celular']

    @method_decorator(permission_required('college.add_division'))
    def dispatch(self, *args, **kwargs):
        return super(DivisionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(DivisionCreateView, self).form_valid(form)


class DivisionDetailView(LoginRequiredMixin, DetailView):

    model = Division
    

class DivisionUpdateView(LoginRequiredMixin, UpdateView):

    model = Division
    #fields = ['nombre','apellido','direccion','ciudad','telefono','celular']
    template_name = "college/division_update_form.html"

    @method_decorator(permission_required('college.change_division'))
    def dispatch(self, *args, **kwargs):
        return super(DivisionUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(DivisionUpdateView, self).form_valid(form)
    

def divisionDeleteView(request, id):
    division = Division.objects.get(pk=id)
    division.delete()
    return HttpResponseRedirect(reverse('divisiones'))


class GestionMateriaDivisionView(LoginRequiredMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''

        user = self.request.user
        tipo_usuario = user.get_tipo()
        if tipo_usuario == 'Alumno': 
            materiasDivision = MateriaDivision.objects.all()
        elif tipo_usuario == 'Profesor':
            materiasDivision = MateriaDivision.objects.all()
        else:
            materiasDivision = MateriaDivision.objects.all()

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            q = Q(materia__nombre__icontains=term_list[0]) | Q(division__nombre__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(materia__nombre__icontains=term) | Q(division__nombre__icontains=term)), q.connector)

            return materiasDivision.filter(q)
        else:
            return materiasDivision


class MateriaDivisionCreateView(LoginRequiredMixin, CreateView):

    model = MateriaDivision

    @method_decorator(permission_required('college.add_calificacion'))
    def dispatch(self, *args, **kwargs):
        return super(MateriaDivisionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(MateriaDivisionCreateView, self).form_valid(form)


class MateriaDivisionDetailView(LoginRequiredMixin, DetailView):

    model = MateriaDivision


class MateriaDivisionUpdateView(LoginRequiredMixin, UpdateView):

    model = MateriaDivision
    #fields = ['nombre','apellido','direccion','ciudad','telefono','celular']
    template_name = "college/materiaDivision_update_form.html"

    @method_decorator(permission_required('college.change_materiadivision'))
    def dispatch(self, *args, **kwargs):
        return super(MateriaDivisionUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(MateriaDivisionUpdateView, self).form_valid(form)
    

def materiaDivisionDeleteView(request, id):
    materiaDivision = MateriaDivision.objects.get(pk=id)
    materiaDivision.delete()
    return HttpResponseRedirect(reverse('materiasdivisiones'))


class GestionCalificacionView(LoginRequiredMixin, ListView):

    paginate_by = 20

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''

        user = self.request.user
        tipo_usuario = user.get_tipo()
        if tipo_usuario == 'Alumno': 
            calificaciones = Calificacion.objects.filter(alumno=user)
        elif tipo_usuario == 'Profesor':
            alumnos = user.profesor.get_alumnos()
            calificaciones = Calificacion.objects.filter(alumno__in=alumnos)
        else:
            calificaciones = Calificacion.objects.all()

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            q = Q(alumno__icontains=term_list[0]) | Q(materia__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(alumno__icontains=term) | Q(materia__icontains=term)), q.connector)

            return calificaciones.filter(q)
        else:
            return calificaciones


class CalificacionCreateView(LoginRequiredMixin, CreateView):

    model = Calificacion

    @method_decorator(permission_required('college.add_calificacion'))
    def dispatch(self, *args, **kwargs):
        return super(CalificacionCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(CalificacionCreateView, self).form_valid(form)


class CalificacionDetailView(LoginRequiredMixin, DetailView):

    model = Calificacion


class CalificacionUpdateView(LoginRequiredMixin, UpdateView):

    model = Calificacion
    #fields = ['nombre','apellido','direccion','ciudad','telefono','celular']
    template_name = "college/calificacion_update_form.html"

    @method_decorator(permission_required('college.change_calificacion'))
    def dispatch(self, *args, **kwargs):
        return super(CalificacionUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(CalificacionUpdateView, self).form_valid(form)
    

def calificacionDeleteView(request, id):
    calificacion = Calificacion.objects.get(pk=id)
    calificacion.delete()
    return HttpResponseRedirect(reverse('calificaciones'))
