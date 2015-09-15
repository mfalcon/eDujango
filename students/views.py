import json

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django import http
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

from students.models import *
from finance.models import Responsable, Autorizado
from students.forms import AlumnoForm, InformeForm

import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import pdb


from django.forms.models import model_to_dict
import forms

@login_required
def students_list(request):
    user = request.user
    tipo = user.empleado.puesto
    if tipo == 3:
        resp = user.empleado.responsable
        students = resp.alumnos.all()
    elif tipo == 2:
        maestra = user.empleado.maestra
        salas_maestra = maestra.salas.all()
        students = []
        for sala in salas_maestra:
            if sala.get_alumnos():
                for alumno in sala.get_alumnos():
                    students.append(alumno)

    else:
        students = Alumno.objects.all()
        

    context = {
        'students' : students, 'tipo': tipo,
    }
    return render_to_response(
        'students/st_list.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def new_student(request):
    if request.method == 'POST':
        form = AlumnoForm(data=request.POST)
        pdb.set_trace()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('st_students_list'))

    else:
        form = AlumnoForm()

    context = {
        'student_form': form,
    }
    return render_to_response(
        'students/st_new_student.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def nuevo_informe(request, st_id):
    st = Alumno.objects.get(pk=st_id)
    if request.method == 'POST':
        form = InformeForm(data=request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.alumno = Alumno.objects.get(pk=st_id)
            informe.maestra = request.user.empleado.maestra
            informe.texto = strip_tags(informe.texto)
            form.save()
            return HttpResponseRedirect(reverse('st_students_list'))

    else:
        form = InformeForm()

    context = {
        'informe_form': form, 'st': st,
    }
    return render_to_response(
        'students/st_nuevo_informe.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def modificar_informe(request, inf_id):
    inf = Informe.objects.get(id=inf_id)
    dictionary = model_to_dict(inf, fields=[], exclude=[])
    #form = forms.InformeForm(dictionary)
    if request.method == 'POST':
        form = InformeForm(data=request.POST)
        if form.is_valid():
            inf.titulo = form.cleaned_data['titulo']
            inf.texto = strip_tags(form.cleaned_data['texto'])
            inf.fecha = form.cleaned_data['fecha']
            inf.save()
            return HttpResponseRedirect(reverse('st_students_list'))

    else:
        form = forms.InformeForm(dictionary)

    context = {
        'informe_form': form,
    }
    return render_to_response(
        'students/st_modificar_informe.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def student_info(request, st_id):
    student = Alumno.objects.get(pk=st_id)

    context = {
        'student': student,
    }
    return render_to_response(
        'students/st_info.html',
         context,
         context_instance = RequestContext(request),
    )

#igual que anterior, solo cambia template
@login_required
def student_personal_info(request, st_id):
    tstudent = Alumno.objects.get(pk=st_id)
    student = AlumnoForm(data=model_to_dict(Alumno.objects.get(pk=st_id)))
    # FIXME arreglar esta negrada
    context = {
        'student': student , 'st': tstudent,
        'tipo': request.user.empleado.puesto,
    }
    return render_to_response(
        'students/st_personal_info.html',
         context,
         context_instance = RequestContext(request),
    )


# vista que se repite
@login_required
def student_reports(request, st_id):
    student = Alumno.objects.get(pk=st_id)

    context = {
        'student': student,
    }
    return render_to_response(
        'students/st_reports.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def student_report(request, inf_id):
    informe = Informe.objects.get(pk=inf_id)

    context = {
        'informe': informe,
    }
    return render_to_response(
        'students/st_report.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def salas(request):
    salas = Sala.objects.all()
    salas_list = []
    for sala in salas:
        conf_varones = sala.alumnosala_set.filter(estado=0, alumno__sexo=0).count()
        conf_nenas = sala.alumnosala_set.filter(estado=0, alumno__sexo=1).count()
        en_espera = sala.alumnosala_set.filter(estado=1).count()
        
        confirmados = conf_varones + conf_nenas

        vacantes = sala.capacidad - confirmados

        salas_list.append([sala, conf_varones, conf_nenas, vacantes, en_espera])


    context = {
        'salas': salas_list,
    }
    return render_to_response(
        'students/salas.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def info_sala(request, sala_id):
    sala = Sala.objects.get(pk=sala_id)

    conf_varones = sala.alumnosala_set.filter(estado=0, alumno__sexo=0)
    conf_nenas = sala.alumnosala_set.filter(estado=0, alumno__sexo=1)
    en_espera = sala.alumnosala_set.filter(estado=1)
    
    confirmados = len(conf_varones) + len(conf_nenas)

    vacantes = sala.capacidad - confirmados

    context = {
        'sala': sala, 'varones': conf_varones, 'nenas': conf_nenas, 'vacantes': vacantes,
        'cant_alumnos': confirmados, 'en_espera': en_espera,
    }
    return render_to_response(
        'students/info_sala.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def  get_informe_as_pdf(request, inf_id):
    i = Informe.objects.get(pk=inf_id) #get_object_or_404

    return write_pdf('students/s_informe_pdf.html',
                { 'i': i, 'pagesize': 'A4'})


def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), \
             mimetype='application/pdf')
    return http.HttpResponse("Error creando el pdf %s" % cgi.escape(html))


def get_hermano_info(request):

    if request.GET and 'hermano_id' in request.GET:

        hermano = Alumno.objects.get(pk=request.GET['hermano_id'])

        responsables = Responsable.objects.filter(alumnos=hermano.pk)
        autorizados = Autorizado.objects.filter(alumnos=hermano.pk)

        response = {'apellido': hermano.apellido, 
                     'responsables':[r.pk for r in responsables],
                     'autorizados': [a.pk for a in autorizados], 'traslado_emergencia':hermano.traslado_emergencia, 
                     'telefono_emergencia':hermano.telefono_emergencia} 

        data = json.dumps(response, cls=DjangoJSONEncoder)
        return HttpResponse(data, mimetype='application/json')