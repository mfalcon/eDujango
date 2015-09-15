# coding: utf-8

# Importaciones Python
from datetime import datetime
import json

# Importaciones Django
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson

# Importaciones Propias
from core.mixins import LoginRequiredMixin
from students.models import Alumno, Sala, AlumnoSala, Maestra
from finance.models import Responsable, Autorizado, Cuota, UnicoPago, \
                           Pago, TipoServicio, ServicioSuscripto, TipoUnicoPago
from efinance.models import Empleado, Honorarios, Sueldo, PagoSueldo, Gasto
from students.forms import ServicioSuscriptoFormSet, \
                           AlumnoSalaFormSet, SalaCrispyForm, MaestraCrispyForm
from finance.forms import ResponsableCrispyForm, AutorizadoCrispyForm, CuotaCrispyForm
from efinance.forms import GastoCrispyForm, EmpleadoCrispyForm, SueldoCrispyForm, PagoSueldoCrispyForm


class GestionAlumnosView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/alumno_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''
        print self.request.user

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            alumnos = Alumno.objects.all()

            q = Q(apellido__icontains=term_list[0]) | Q(nombre1__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(apellido__icontains=term) | Q(nombre1__icontains=term)), q.connector)

            return alumnos.filter(q)
        else:
            return Alumno.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionAlumnosView, self).get_context_data(**kwargs)
        context['salas'] = Sala.objects.all()
        return context


class AlumnoCreateView(LoginRequiredMixin, CreateView):

    model = Alumno
    template_name = "jardin/alumno_form.html"

    @method_decorator(permission_required('student.add_alumno'))
    def dispatch(self, *args, **kwargs):
        return super(AlumnoCreateView, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioSuscriptoFormSet()
        alumnoSala_form = AlumnoSalaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  servicio_form=servicio_form,
                                  alumnoSala_form=alumnoSala_form))

    def post(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioSuscriptoFormSet(self.request.POST, instance=self.object)
        alumnoSala_form = AlumnoSalaFormSet(self.request.POST, instance=self.object)

        if (form.is_valid() and servicio_form.is_valid() and alumnoSala_form.is_valid()):
            return self.form_valid(form, servicio_form, alumnoSala_form)
        else:
            return self.form_invalid(form, servicio_form, alumnoSala_form)

    def form_valid(self, form, servicio_form, alumnoSala_form):
        #self.object = form.save()
        alumno = form.save(commit=False)
        alumno.save()


        total_salas =  int(self.request.POST.get('alumnosala_set-TOTAL_FORMS'))
        for x in range(0,total_salas):
            sala_id = self.request.POST.get('alumnosala_set-'+str(x)+'-sala')
            estado = self.request.POST.get('alumnosala_set-'+str(x)+'-estado')
            comentarios = self.request.POST.get('alumnosala_set-'+str(x)+'-comentarios')
            sala = Sala.objects.get(pk=sala_id)
            p = AlumnoSala(alumno=alumno, estado=estado,sala=sala,comentarios=comentarios)
            p.save()
        import pdb; pdb.set_trace()
        self.object = form.save()
        servicio_form.instance = self.object
        servicio_form.save()
        alumnoSala_form.instance = self.object
        alumnoSala_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, servicio_form, alumnoSala_form):

        return self.render_to_response(
            self.get_context_data(form=form,
                                  servicio_form=servicio_form,
                                  alumnoSala_form=alumnoSala_form))




class AlumnoDetailView(LoginRequiredMixin, DetailView):

    model = Alumno
    template_name = "jardin/alumno_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(AlumnoDetailView, self).get_context_data(**kwargs)
        context['st_debt'] = self.object.get_deuda()
        context['unpaid_cuotas'] = Cuota.objects.filter(alumno=self.object, paga=False)
        context['unpaid_unicos'] = UnicoPago.objects.filter(alumno=self.object, paga=False)
        context['st_last_payments'] = self.object.last_payments(5)
        return context


class AlumnoUpdateView(LoginRequiredMixin, UpdateView):

    model = Alumno
    template_name = "jardin/alumno_update_form.html"

    @method_decorator(permission_required('student.change_alumno'))
    def dispatch(self, *args, **kwargs):
        return super(AlumnoUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        self.object = Alumno.objects.get(pk=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioSuscriptoFormSet()
        alumnoSala_form = AlumnoSalaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  servicio_form=servicio_form,
                                  alumnoSala_form=alumnoSala_form))

    def post(self, request, *args, **kwargs):

        self.object = Alumno.objects.get(pk=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        servicio_form = ServicioSuscriptoFormSet(self.request.POST, instance=self.object)
        alumnoSala_form = AlumnoSalaFormSet(self.request.POST, instance=self.object)

        if (form.is_valid() and servicio_form.is_valid() and alumnoSala_form.is_valid()):
            return self.form_valid(form, servicio_form, alumnoSala_form)
        else:
            return self.form_invalid(form, servicio_form, alumnoSala_form)

    def form_valid(self, form, servicio_form, alumnoSala_form):

        self.object = form.save(commit=False)
        #for x in range(0,len(self.object)):
        #    for y in self.request.POST.getlist('alumnosala_set-'+str(x)+'-sala'):
        #        sala = Sala.objects.get(pk=y)
        #        p=AlumnoSala(alumno=self.object.pk, estado=0,sala=sala)
        #        p.save()
        self.object = form.save()
        servicio_form.instance = self.object
        servicio_form.save()
        alumnoSala_form.instance = self.object
        alumnoSala_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, servicio_form, alumnoSala_form):

        return self.render_to_response(
            self.get_context_data(form=form,
                                  servicio_form=servicio_form,
                                  alumnoSala_form=alumnoSala_form))
    

def alumnoDeleteView(request, id):
    alumno = Alumno.objects.get(pk=id)
    alumno.delete()
    return HttpResponseRedirect(reverse('alumnos'))


class GestionResponsableView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/responsable_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''
        print self.request.user

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            responsables = Responsable.objects.all()

            q = Q(last_name__icontains=term_list[0]) | Q(first_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(last_name__icontains=term) | Q(first_name__icontains=term)), q.connector)

            return responsables.filter(q)
        else:
            return Responsable.objects.all()


class ResponsableCreateView(LoginRequiredMixin, CreateView):

    model = Responsable
    template_name = "jardin/responsable_form.html"
    form_class = ResponsableCrispyForm
    fields = ['password','tipo_doc', 'num_doc', 'email','first_name', 
                  'second_name', 'last_name', 'sexo', 'fecha_nac', 'domicilio',
                  'localidad', 'telefono', 'nacionalidad', 'relacion', 'telefono_laboral1',
                  'telefono_laboral2', 'como_conocio', 'ocupacion']

    @method_decorator(permission_required('finance.add_alumno'))
    def dispatch(self, *args, **kwargs):
        return super(ResponsableCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(ResponsableCreateView, self).form_valid(form)


class ResponsableDetailView(LoginRequiredMixin, DetailView):

    model = Responsable
    template_name = "jardin/responsable_detail.html"


class ResponsableUpdateView(LoginRequiredMixin, UpdateView):

    model = Responsable
    template_name = "jardin/responsable_update_form.html"
    form_class = ResponsableCrispyForm
    fields = ['password', 'tipo_doc', 'num_doc', 'email','first_name', 
                  'second_name', 'last_name', 'sexo', 'fecha_nac', 'domicilio',
                  'localidad', 'telefono', 'nacionalidad', 'relacion', 'telefono_laboral1',
                  'telefono_laboral2', 'como_conocio']


    @method_decorator(permission_required('finance.change_responsable'))
    def dispatch(self, *args, **kwargs):
        return super(ResponsableUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(ResponsableUpdateView, self).form_valid(form)
    

def responsableDeleteView(request, id):
    responsable = Responsable.objects.get(pk=id)
    responsable.delete()
    return HttpResponseRedirect(reverse('responsables'))


class GestionAutorizadoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/autorizado_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''
        print self.request.user

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            autorizados = Autorizado.objects.all()

            q = Q(last_name__icontains=term_list[0]) | Q(first_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(last_name__icontains=term) | Q(first_name__icontains=term)), q.connector)

            return autorizados.filter(q)
        else:
            return Autorizado.objects.all()


class AutorizadoCreateView(LoginRequiredMixin, CreateView):

    model = Autorizado
    template_name = "jardin/autorizado_form.html"
    form_class = AutorizadoCrispyForm

    @method_decorator(permission_required('finance.add_autorizado'))
    def dispatch(self, *args, **kwargs):
        return super(AutorizadoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(AutorizadoCreateView, self).form_valid(form)


class AutorizadoDetailView(LoginRequiredMixin, DetailView):

    model = Autorizado
    template_name = "jardin/autorizado_detail.html"


class AutorizadoUpdateView(LoginRequiredMixin, UpdateView):

    model = Autorizado
    template_name = "jardin/autorizado_update_form.html"

    fields = ['password', 'tipo_doc', 'num_doc','email','first_name', 
              'second_name', 'last_name', 'sexo', 'fecha_nac', 'domicilio',
              'localidad', 'telefono', 'nacionalidad', 'relacion', 'otra']

    @method_decorator(permission_required('finance.change_autorizado'))
    def dispatch(self, *args, **kwargs):
        return super(AutorizadoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(AutorizadoUpdateView, self).form_valid(form)
    

def autorizadoDeleteView(request, id):
    autorizado = Autorizado.objects.get(pk=id)
    autorizado.delete()
    return HttpResponseRedirect(reverse('autorizados'))


class GestionSalaView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/sala_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los profesores
        '''
        print self.request.user

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            salas = Sala.objects.all()

            q = Q(sala__icontains=term_list[0]) | Q(turno__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(sala__icontains=term) | Q(turno__icontains=term)), q.connector)

            return salas.filter(q)
        else:
            return Sala.objects.all()


class SalaCreateView(LoginRequiredMixin, CreateView):

    model = Sala
    template_name = "jardin/sala_form.html"
    form_class = SalaCrispyForm

    @method_decorator(permission_required('student.add_sala'))
    def dispatch(self, *args, **kwargs):
        return super(SalaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(SalaCreateView, self).form_valid(form)


class SalaDetailView(LoginRequiredMixin, DetailView):

    model = Sala
    template_name = "jardin/sala_detail.html"
    context_object_name = "sala"

    def get_context_data(self, **kwargs):
        context = super(SalaDetailView, self).get_context_data(**kwargs)


        conf_varones = self.object.alumnosala_set.filter(estado=0, alumno__sexo=0)
        conf_nenas = self.object.alumnosala_set.filter(estado=0, alumno__sexo=1)
        en_espera = self.object.alumnosala_set.filter(estado=1)
        
        confirmados = len(conf_varones) + len(conf_nenas)

        vacantes = self.object.capacidad - confirmados

        context['varones'] = conf_varones
        context['nenas'] = conf_nenas
        context['vacantes'] = vacantes
        context['cant_alumnos'] = confirmados
        context['en_espera'] = en_espera
        return context

class SalaUpdateView(LoginRequiredMixin, UpdateView):

    model = Sala
    template_name = "jardin/sala_update_form.html"
    form_class = SalaCrispyForm

    @method_decorator(permission_required('student.change_sala'))
    def dispatch(self, *args, **kwargs):
        return super(SalaUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(SalaUpdateView, self).form_valid(form)
    

def salaDeleteView(request, id):
    sala = Sala.objects.get(pk=id)
    sala.delete()
    return HttpResponseRedirect(reverse('salas'))



# TODO
# ver de usar user_passes_test o permission_required
# https://docs.djangoproject.com/en/1.5/topics/auth/default/

@login_required
def insertar_arancel(request):
    """
        Recibe un monto y una lista de id's de alumnos
        para asignarle un arancel
    """

    if request.GET and request.GET['monto'] and request.GET['ids'] and request.GET['concepto']:

        try:
            ids = request.GET['ids'].split(",")
            monto = request.GET['monto']
            concepto = request.GET['concepto']

            alumnos = Alumno.objects.filter(pk__in=ids)
        
            for alumno in alumnos:
                cuota = Cuota(alumno=alumno, importe=monto, deuda=monto,
                             fecha=datetime.today(), paga=False, concepto=concepto)
                cuota.save()


            data = json.dumps({'resultado':True}, cls=DjangoJSONEncoder)
            return HttpResponse(data, mimetype='application/json')
        except:
            data = json.dumps({'resultado':False}, cls=DjangoJSONEncoder)
            return HttpResponse(data, mimetype='application/json')


@login_required
def cambiar_division(request):
    """
        Recibe una lista de id's de alumnos
        para cambiar division
    """

    if request.GET and request.GET['ids'] and request.GET['sala1'] and request.GET['sala2']:
        try:
            ids = request.GET['ids'].split(",")
            id_sala_1 = int(request.GET['sala1'])
            id_sala_2 = int(request.GET['sala2'])

            alumnos = Alumno.objects.filter(pk__in=ids)


            if id_sala_1 != 0:
                sala_1 = Sala.objects.get(pk=id_sala_1) 
            if id_sala_2 != 0:
                sala_2 = Sala.objects.get(pk=id_sala_2) 
            
            for alumno in alumnos:
                # Elimina las salas que tiene
                alumno.sala.clear()
                # Crea las AlumnoSala
                if id_sala_1 != 0:
                    as1 = AlumnoSala(alumno=alumno,sala=sala_1,estado=1)
                    as1.save()
                if id_sala_2 != 0:
                    print "alalalalalal"
                    as2 = AlumnoSala(alumno=alumno,sala=sala_2,estado=1)
                    as2.save()
                alumno.save()
            
            data = json.dumps({'resultado':True}, cls=DjangoJSONEncoder)
            return HttpResponse(data, mimetype='application/json')
        except:
            data = json.dumps({'resultado':False}, cls=DjangoJSONEncoder)
            return HttpResponse(data, mimetype='application/json')


class GestionEmpleadoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/empleado_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los empleados
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            empelados = Empleado.objects.all()

            q = Q(first_name__icontains=term_list[0]) | Q(last_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(first_name__icontains=term) | Q(last_name__icontains=term)), q.connector)

            return empelados.filter(q)
        else:
            return Empleado.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionEmpleadoView, self).get_context_data(**kwargs)
        return context


class EmpleadoCreateView(LoginRequiredMixin, CreateView):

    model = Empleado
    form_class = EmpleadoCrispyForm
    template_name = "jardin/empleado_form.html"

    fields = ['password', 'groups','tipo_doc', 'num_doc', 'email', 'first_name', 'second_name',
              'last_name', 'sexo', 'fecha_nac', 'domicilio', 'localidad', 'telefono', 
              'nacionalidad', 'puesto']

    @method_decorator(permission_required('efinance.add_empleado'))
    def dispatch(self, *args, **kwargs):
        return super(EmpleadoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(EmpleadoCreateView, self).form_valid(form)


class EmpleadoDetailView(LoginRequiredMixin, DetailView):

    model = Empleado
    template_name = "jardin/empleado_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        return context


class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):

    model = Empleado
    template_name = "jardin/empleado_update_form.html"
    form_class = EmpleadoCrispyForm

    fields = ['password', 'groups','tipo_doc', 'num_doc', 'email', 'first_name', 'second_name',
              'last_name', 'sexo', 'fecha_nac', 'domicilio', 'localidad', 'telefono', 
              'nacionalidad', 'puesto']
              
    @method_decorator(permission_required('efinance.change_empleado'))
    def dispatch(self, *args, **kwargs):
        return super(EmpleadoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(EmpleadoUpdateView, self).form_valid(form)
    

def empleadoDeleteView(request, id):
    empleado = Empleado.objects.get(pk=id)
    empleado.delete()
    return HttpResponseRedirect(reverse('empleados'))


class GestionMaestraView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/maestra_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todas las maestras
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            maestras = Maestra.objects.all()

            q = Q(first_name__icontains=term_list[0]) | Q(last_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(first_name__icontains=term) | Q(last_name__icontains=term)), q.connector)

            return maestras.filter(q)
        else:
            return Maestra.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionMaestraView, self).get_context_data(**kwargs)
        return context


class MaestraCreateView(LoginRequiredMixin, CreateView):

    model = Maestra
    template_name = "jardin/maestra_form.html"
    form_class = MaestraCrispyForm

    @method_decorator(permission_required('student.add_maestra'))
    def dispatch(self, *args, **kwargs):
        return super(MaestraCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        self.object = form.save(commit=False)  
        self.object.puesto = 2
        self.object = form.save()  
        self.object.save()
        return super(MaestraCreateView, self).form_valid(form)


class MaestraDetailView(LoginRequiredMixin, DetailView):

    model = Maestra
    template_name = "jardin/maestra_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(MaestraDetailView, self).get_context_data(**kwargs)
        return context


class MaestraUpdateView(LoginRequiredMixin, UpdateView):

    model = Maestra
    template_name = "jardin/maestra_update_form.html"
    form_class = MaestraCrispyForm
              
    @method_decorator(permission_required('student.change_maestra'))
    def dispatch(self, *args, **kwargs):
        return super(MaestraUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False) 
        self.object.puesto = 2 
        self.object = form.save()  
        self.object.save()
        return super(MaestraUpdateView, self).form_valid(form)
    
def maestraDeleteView(request, id):
    maestra = Maestra.objects.get(pk=id)
    maestra.delete()
    return HttpResponseRedirect(reverse('maestra'))


class GestionHonorarioView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/honorario_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los honorarios
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            honorarios = Honorarios.objects.all()

            q = Q(empleado__first_name__icontains=term_list[0]) | Q(empleado__last_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(empleado__first_name__icontains=term) | Q(empleado__last_name__icontains=term)), q.connector)

            return honorarios.filter(q)
        else:
            return Honorarios.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionHonorarioView, self).get_context_data(**kwargs)
        return context


class HonorarioCreateView(LoginRequiredMixin, CreateView):

    model = Honorarios
    template_name = "jardin/honorario_form.html"


    @method_decorator(permission_required('efinance.add_honorarios'))
    def dispatch(self, *args, **kwargs):
        return super(HonorarioCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(HonorarioCreateView, self).form_valid(form)


class HonorarioDetailView(LoginRequiredMixin, DetailView):

    model = Honorarios
    template_name = "jardin/honorario_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HonorarioDetailView, self).get_context_data(**kwargs)
        return context


class HonorarioUpdateView(LoginRequiredMixin, UpdateView):

    model = Honorarios
    template_name = "jardin/honorario_update_form.html"

    @method_decorator(permission_required('efinance.change_honorarios'))
    def dispatch(self, *args, **kwargs):
        return super(HonorarioUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(HonorarioUpdateView, self).form_valid(form)
    
def honorarioDeleteView(request, id):
    honorario = Honorarios.objects.get(pk=id)
    honorario.delete()
    return HttpResponseRedirect(reverse('honorarios-jardin'))


class GestionSueldoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/sueldo_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los sueldos
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            sueldos = Sueldo.objects.all()

            q = Q(empleado__first_name__icontains=term_list[0]) | Q(empleado__last_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(empleado__first_name__icontains=term) | Q(empleado__last_name__icontains=term)), q.connector)

            return sueldos.filter(q)
        else:
            return Sueldo.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionSueldoView, self).get_context_data(**kwargs)
        return context


class SueldoCreateView(LoginRequiredMixin, CreateView):

    model = Sueldo
    template_name = "jardin/sueldo_form.html"
    form_class = SueldoCrispyForm

    @method_decorator(permission_required('efinance.add_sueldo'))
    def dispatch(self, *args, **kwargs):
        return super(SueldoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(SueldoCreateView, self).form_valid(form)


class SueldoDetailView(LoginRequiredMixin, DetailView):

    model = Sueldo
    template_name = "jardin/sueldo_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SueldoDetailView, self).get_context_data(**kwargs)
        return context


class SueldoUpdateView(LoginRequiredMixin, UpdateView):

    model = Sueldo
    template_name = "jardin/sueldo_update_form.html"
    form_class = SueldoCrispyForm

    @method_decorator(permission_required('efinance.change_sueldo'))
    def dispatch(self, *args, **kwargs):
        return super(SueldoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(SueldoUpdateView, self).form_valid(form)
    
def sueldoDeleteView(request, id):
    sueldo = Sueldo.objects.get(pk=id)
    sueldo.delete()
    return HttpResponseRedirect(reverse('sueldos-jardin'))


class GestionPagoSueldoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/pagosueldo_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los pagos
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            pagos = PagoSueldo.objects.all()

            q = Q(empleado__first_name__icontains=term_list[0]) | Q(empleado__last_name__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(empleado__first_name__icontains=term) | Q(empleado__last_name__icontains=term)), q.connector)

            return pagos.filter(q)
        else:
            return PagoSueldo.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionPagoSueldoView, self).get_context_data(**kwargs)
        return context


class PagoSueldoCreateView(LoginRequiredMixin, CreateView):

    model = PagoSueldo
    template_name = "jardin/pagosueldo_form.html"
    form_class = PagoSueldoCrispyForm


    @method_decorator(permission_required('efinance.add_pagosueldo'))
    def dispatch(self, *args, **kwargs):
        return super(PagoSueldoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(PagoSueldoCreateView, self).form_valid(form)


class PagoSueldoDetailView(LoginRequiredMixin, DetailView):

    model = PagoSueldo
    template_name = "jardin/pagosueldo_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PagoSueldoDetailView, self).get_context_data(**kwargs)
        return context


class PagoSueldoUpdateView(LoginRequiredMixin, UpdateView):

    model = PagoSueldo
    template_name = "jardin/pagosueldo_update_form.html"
    form_class = PagoSueldoCrispyForm

    @method_decorator(permission_required('efinance.change_pagosueldo'))
    def dispatch(self, *args, **kwargs):
        return super(PagoSueldoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(PagoSueldoUpdateView, self).form_valid(form)
    
def pagosueldoDeleteView(request, id):
    pago = PagoSueldo.objects.get(pk=id)
    pago.delete()
    return HttpResponseRedirect(reverse('pagos-jardin'))


class GestionTipoServicioView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/tiposervicio_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los tipos de servicio
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            tipos = TipoServicio.objects.all()

            q = Q(tipo__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(tipo__first_name__icontains=term)), q.connector)

            return tipos.filter(q)
        else:
            return TipoServicio.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionTipoServicioView, self).get_context_data(**kwargs)
        return context


class TipoServicioCreateView(LoginRequiredMixin, CreateView):

    model = TipoServicio
    template_name = "jardin/tiposervicio_form.html"


    @method_decorator(permission_required('finance.add_tiposervicio'))
    def dispatch(self, *args, **kwargs):
        return super(TipoServicioCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(TipoServicioCreateView, self).form_valid(form)


class TipoServicioDetailView(LoginRequiredMixin, DetailView):

    model = TipoServicio
    template_name = "jardin/tiposervicio_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(TipoServicioDetailView, self).get_context_data(**kwargs)
        return context


class TipoServicioUpdateView(LoginRequiredMixin, UpdateView):

    model = TipoServicio
    template_name = "jardin/tiposervicio_update_form.html"

    @method_decorator(permission_required('finance.change_tiposervicio'))
    def dispatch(self, *args, **kwargs):
        return super(TipoServicioUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(TipoServicioUpdateView, self).form_valid(form)
    
def tiposervicioDeleteView(request, id):
    tipo = TipoServicio.objects.get(pk=id)
    tipo.delete()
    return HttpResponseRedirect(reverse('tipo-servicios-jardin'))


class GestionServicioSuscriptoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/serviciosuscripto_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los servicios
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            servicios = ServicioSuscripto.objects.all()

            q = Q(tipo__tipo__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(tipo__tipo__icontains=term)), q.connector)

            return servicios.filter(q)
        else:
            return ServicioSuscripto.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionServicioSuscriptoView, self).get_context_data(**kwargs)
        return context


class ServicioSuscriptoCreateView(LoginRequiredMixin, CreateView):

    model = ServicioSuscripto
    template_name = "jardin/serviciosuscripto_form.html"


    @method_decorator(permission_required('finance.add_serviciosuscripto'))
    def dispatch(self, *args, **kwargs):
        return super(ServicioSuscriptoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(ServicioSuscriptoCreateView, self).form_valid(form)


class ServicioSuscriptoDetailView(LoginRequiredMixin, DetailView):

    model = ServicioSuscripto
    template_name = "jardin/serviciosuscripto_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ServicioSuscriptoDetailView, self).get_context_data(**kwargs)
        return context


class ServicioSuscriptoUpdateView(LoginRequiredMixin, UpdateView):

    model = ServicioSuscripto
    template_name = "jardin/serviciosuscripto_update_form.html"

    @method_decorator(permission_required('finance.change_serviciosuscripto'))
    def dispatch(self, *args, **kwargs):
        return super(ServicioSuscriptoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(ServicioSuscriptoUpdateView, self).form_valid(form)
    
def serviciosuscriptoDeleteView(request, id):
    servicio = ServicioSuscripto.objects.get(pk=id)
    servicio.delete()
    return HttpResponseRedirect(reverse('servicios-jardin'))


class GestionTipoUnicoPagoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    template_name = "jardin/tipounicopago_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los tipos de pago unico
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            tipos = TipoUnicoPago.objects.all()

            q = Q(tipo__tipo__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(tipo__tipo__icontains=term)), q.connector)

            return tipos.filter(q)
        else:
            return TipoUnicoPago.objects.all()


    def get_context_data(self, **kwargs):
        context = super(GestionTipoUnicoPagoView, self).get_context_data(**kwargs)
        return context


class TipoUnicoPagoCreateView(LoginRequiredMixin, CreateView):

    model = TipoUnicoPago
    template_name = "jardin/tipounicopago_form.html"


    @method_decorator(permission_required('finance.add_tipounicopago'))
    def dispatch(self, *args, **kwargs):
        return super(TipoUnicoPagoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(TipoUnicoPagoCreateView, self).form_valid(form)


class TipoUnicoPagoDetailView(LoginRequiredMixin, DetailView):

    model = TipoUnicoPago
    template_name = "jardin/tipounicopago_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(TipoUnicoPagoDetailView, self).get_context_data(**kwargs)
        return context


class TipoUnicoPagoUpdateView(LoginRequiredMixin, UpdateView):

    model = TipoUnicoPago
    template_name = "jardin/tipounicopago_update_form.html"

    @method_decorator(permission_required('finance.change_tipounicopago'))
    def dispatch(self, *args, **kwargs):
        return super(TipoUnicoPagoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(TipoUnicoPagoUpdateView, self).form_valid(form)
    
def tipounicopagoDeleteView(request, id):
    tipo = TipoUnicoPago.objects.get(pk=id)
    tipo.delete()
    return HttpResponseRedirect(reverse('tipos-pagos-unico-jardin'))


class GestionGastoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    model = Gasto
    template_name = "jardin/gasto_list.html"

    def get_context_data(self, **kwargs):
        context = super(GestionGastoView, self).get_context_data(**kwargs)
        return context


class GastoCreateView(LoginRequiredMixin, CreateView):

    model = Gasto
    template_name = "jardin/gasto_form.html"
    form_class = GastoCrispyForm

    @method_decorator(permission_required('efinance.add_gasto'))
    def dispatch(self, *args, **kwargs):
        return super(GastoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(GastoCreateView, self).form_valid(form)


class GastoDetailView(LoginRequiredMixin, DetailView):

    model = Gasto
    template_name = "jardin/gasto_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(GastoDetailView, self).get_context_data(**kwargs)
        return context


class GastoUpdateView(LoginRequiredMixin, UpdateView):

    model = Gasto
    template_name = "jardin/gasto_update_form.html"
    form_class = GastoCrispyForm

    @method_decorator(permission_required('efinance.change_gasto'))
    def dispatch(self, *args, **kwargs):
        return super(GastoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(GastoUpdateView, self).form_valid(form)
    
def gastoDeleteView(request, id):
    gasto = Gasto.objects.get(pk=id)
    gasto.delete()
    return HttpResponseRedirect(reverse('gasto-jardin'))


class GestionCuotaView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    model = Cuota
    template_name = "jardin/cuota_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todas las cuotas 
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            cuotas = Cuota.objects.all()

            q = Q(alumno__nombre1__icontains=term_list[0]) | Q(alumno__apellido__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(alumno__nombre1__icontains=term) | Q(alumno__apellido__icontains=term)), q.connector)

            return cuotas.filter(q)
        else:
            return Cuota.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GestionCuotaView, self).get_context_data(**kwargs)
        return context


class CuotaCreateView(LoginRequiredMixin, CreateView):

    model = Cuota
    form_class = CuotaCrispyForm
    template_name = "jardin/cuota_form.html"


    @method_decorator(permission_required('finance.add_cuota'))
    def dispatch(self, *args, **kwargs):
        return super(CuotaCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(CuotaCreateView, self).form_valid(form)


class CuotaDetailView(LoginRequiredMixin, DetailView):

    model = Cuota
    template_name = "jardin/cuota_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(CuotaDetailView, self).get_context_data(**kwargs)
        return context


class CuotaUpdateView(LoginRequiredMixin, UpdateView):

    model = Cuota
    template_name = "jardin/cuota_update_form.html"
    form_class = CuotaCrispyForm

    @method_decorator(permission_required('finance.change_cuota'))
    def dispatch(self, *args, **kwargs):
        return super(CuotaUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(CuotaUpdateView, self).form_valid(form)
    
def cuotaDeleteView(request, id):
    cuota = Cuota.objects.get(pk=id)
    cuota.delete()
    return HttpResponseRedirect(reverse('cuota-jardin'))


class GestionPagoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    model = Pago
    template_name = "jardin/pago_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los pagos
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            pagos = Pago.objects.all()

            q = Q(alumno__nombre1__icontains=term_list[0]) | Q(alumno__apellido__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(alumno__nombre1__icontains=term) | Q(alumno__apellido__icontains=term)), q.connector)

            return pagos.filter(q)
        else:
            return Pago.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GestionPagoView, self).get_context_data(**kwargs)
        return context


class PagoCreateView(LoginRequiredMixin, CreateView):

    model = Pago
    template_name = "jardin/pago_form.html"


    @method_decorator(permission_required('finance.add_pago'))
    def dispatch(self, *args, **kwargs):
        return super(PagoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(PagoCreateView, self).form_valid(form)


class PagoDetailView(LoginRequiredMixin, DetailView):

    model = Pago
    template_name = "jardin/pago_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PagoDetailView, self).get_context_data(**kwargs)
        return context


class PagoUpdateView(LoginRequiredMixin, UpdateView):

    model = Pago
    template_name = "jardin/pago_update_form.html"

    @method_decorator(permission_required('finance.change_pago'))
    def dispatch(self, *args, **kwargs):
        return super(PagoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(PagoUpdateView, self).form_valid(form)
    
def pagoDeleteView(request, id):
    pago = Pago.objects.get(pk=id)
    pago.delete()
    return HttpResponseRedirect(reverse('pago-jardin'))


class GestionPagoUnicoView(LoginRequiredMixin, ListView):
    
    paginate_by = 20
    model = Pago
    template_name = "jardin/pagounico_list.html"

    def get_queryset(self):
        '''
        Filtra por los terminos en el campo de busqueda, si no se busca por nada
        devuelve todos los pagos unicos
        '''

        if self.request.GET.get('terms'):
            terms = self.request.GET.get('terms', None)
            term_list = terms.split(' ')

            pagos = UnicoPago.objects.all()

            q = Q(alumno__nombre1__icontains=term_list[0]) | Q(alumno__apellido__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(alumno__nombre1__icontains=term) | Q(alumno__apellido__icontains=term)), q.connector)

            return pagos.filter(q)
        else:
            return UnicoPago.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GestionPagoUnicoView, self).get_context_data(**kwargs)
        return context


class PagoUnicoCreateView(LoginRequiredMixin, CreateView):

    model = UnicoPago
    template_name = "jardin/pagounico_form.html"


    @method_decorator(permission_required('finance.add_unicopago'))
    def dispatch(self, *args, **kwargs):
        return super(PagoUnicoCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(PagoUnicoCreateView, self).form_valid(form)


class PagoUnicoDetailView(LoginRequiredMixin, DetailView):

    model = UnicoPago
    template_name = "jardin/pagounico_detail.html"

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PagoUnicoDetailView, self).get_context_data(**kwargs)
        return context


class PagoUnicoUpdateView(LoginRequiredMixin, UpdateView):

    model = UnicoPago
    template_name = "jardin/pagounico_update_form.html"

    @method_decorator(permission_required('finance.change_unicopago'))
    def dispatch(self, *args, **kwargs):
        return super(PagoUnicoUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()  
        self.object.save()
        return super(PagoUnicoUpdateView, self).form_valid(form)
    
def pagounicoDeleteView(request, id):
    unicopago = UnicoPago.objects.get(pk=id)
    unicopago.delete()
    return HttpResponseRedirect(reverse('unicopago-jardin'))


