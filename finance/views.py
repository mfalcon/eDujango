from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse,HttpResponseBadRequest
from django import http
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from finance.models import *
from finance.forms import PagoForm, ServicioSuscriptoForm, UnicoPagoForm
from finance.settings import SIN_CUOTA, PUN_CUOTAS
from finance.utils import generate_payments, realizar_pago

from students.models import Alumno
from easy_pdf.views import PDFTemplateView

import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django_xhtml2pdf.utils import generate_pdf

from datetime import date
import json


@login_required
def monthly_payments(request):
    already_generated = generate_payments()

    context = {
        'already_generated': already_generated,
    }
    return render_to_response(
        'finance/f_payments.html',
        context,
        context_instance = RequestContext(request),
    )


@login_required
def students(request):
    students = Alumno.objects.all()
    deudas_cuotas = sum([c.deuda for c in Cuota.objects.filter(paga=False)])

    context = {
        'students': students, 'deuda': deudas_cuotas,
    }
    return render_to_response(
        'finance/f_students.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def modificar_pago(request, pago_id):
    pago = Pago.objects.get(pk=pago_id)
    student = pago.alumno
    st_debt = student.get_deuda()
    dictionary = model_to_dict(pago, fields=[], exclude=[])

    if request.method == 'POST':
        form = PagoForm(student=student, data=request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.alumno = student
            realizar_pago(payment.abona, student.id)
            payment.save()
            #return HttpResponseRedirect(reverse('f_students'))
            return HttpResponseRedirect(reverse('f_student_report', args=[payment.id]))

    else:
        form = PagoForm(dictionary,student=student)

    context = {
        'form': form, 'st': student, 'st_debt': st_debt,
    }
    return render_to_response(
        'finance/f_modificar_pago.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def new_service(request, st_id):
    student = Alumno.objects.get(pk=st_id)

    if request.method == 'POST':
        form = ServicioSuscriptoForm(st=student, data=request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.alumno = student
            if service.importe == None:
                service.importe = TipoServicio.objects.get(tipo=service.tipo.tipo).importe # TO FIX
            service.save()
            #return HttpResponseRedirect(reverse('f_students'))
            return HttpResponseRedirect(reverse('f_students'))

    else:
        form = ServicioSuscriptoForm(st=student)

    context = {
        'form': form, 'st': student,
    }
    return render_to_response(
        'finance/f_new_service.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def new_unique_payment(request, st_id):
    student = Alumno.objects.get(pk=st_id)

    if request.method == 'POST':
        form = UnicoPagoForm(st=student, data=request.POST)
        if form.is_valid():
            fpu = form.save(commit=False)
            alumno = student
            if not fpu.importe:
                importe = TipoUnicoPago.objects.get(tipo=fpu.tipo.tipo).importe # TO FIX
            else:
                importe = fpu.importe
            deuda = importe
            UnicoPago.objects.create(alumno=alumno, importe=importe, deuda=deuda, tipo=fpu.tipo
                , responsable=fpu.responsable)
            
            
            return HttpResponseRedirect(reverse('f_students'))
        else:
            if request.is_ajax():
                # Prepare JSON for parsing
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)

                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                # render() form with errors (No AJAX)
                pass
            
    else:
        form = UnicoPagoForm(st=student)

    context = {
        'form': form, 'st': student,
    }
    return render_to_response(
        'finance/f_new_unique_payment.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def f_student_info(request, st_id):
    student = Alumno.objects.get(pk=st_id)
    st_debt = student.get_deuda()
    unpaid_cuotas = Cuota.objects.filter(alumno=st_id, paga=False)
    unpaid_unicos = UnicoPago.objects.filter(alumno=st_id, paga=False)
    '''
    for uc in unpaid_cuotas:
        fecha_origen = uc.fecha
        hoy = date.today
        #days_difference = TODO
        import pdb; pdb.set_trace()
    '''
    #unpaid_uniques = UnicoPago.objects.filter(alumno=st_id, paga=False)
    st_last_payments = student.last_payments(5)

    context = {
        'student' : student,
        'st_debt' : st_debt,
        'st_last_payments' : st_last_payments,
        'unpaid_cuotas': unpaid_cuotas,
        'unpaid_unicos': unpaid_unicos,
    }
    return render_to_response(
        'finance/f_student_info.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def new_payment(request, st_id):
    student = Alumno.objects.get(pk=st_id)
    st_debt = student.get_deuda()
    unpaid_cuotas = Cuota.objects.filter(alumno=st_id, paga=False)
    unpaid_unicos = UnicoPago.objects.filter(alumno=st_id, paga=False)

    if request.method == 'POST':
        form = PagoForm(student=student, data=request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.alumno = student
            servicios_pagados = realizar_pago(payment.abona, student.id)
            #modificar pago(pago anterior, pago actual, student id)
            payment.save()
            for item in servicios_pagados:
                #FIXME: las cuotas se guardan con el total del pago - ver descarga(30).pdf
                it = ItemPago(pago=payment, importe=item[1], descripcion=item[0])
                it.save()

            if request.is_ajax():
                response = [{'pdf':reverse('f_student_report_nuevo', args=[payment.id]), 'success': reverse('f_students')}] 
                data = json.dumps(response, cls=DjangoJSONEncoder)
                return HttpResponse(data, mimetype='application/json')
        else:
            if request.is_ajax():
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)

                return HttpResponseBadRequest(json.dumps(errors_dict))
            
    else:
        form = PagoForm(student=student)

    context = {
        'form': form, 'st': student, 'st_debt': st_debt,
        'unpaid_cuotas': unpaid_cuotas, 'unpaid_unicos': unpaid_unicos,
    }
    return render_to_response(
        'finance/f_new_payment.html',
         context,
         context_instance = RequestContext(request),
    )




class ReportPDFView(PDFTemplateView):

    template_name = "finance/f_student_report_nuevo.html"

    def get_context_data(self, **kwargs):
        pago = Pago.objects.get(pk=self.kwargs['pago_id']) #get_object_or_404
        student = pago.alumno
        student_services = student.suscript_services() #servicios suscriptos-no muestra pagos unicos realizados
        fecha = date.today()
        comentarios = pago.comentarios

        items = ItemPago.objects.filter(pago=pago.id)

        return super(ReportPDFView, self).get_context_data(
            pagesize="A4",
            students=student,
            services=student_services,
            items=items,
            pago=pago,
            fecha=fecha,
            comentarios=comentarios,
            **kwargs
        )
   


from functools import wraps
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

def permanent_redirect(url):
    """
    Executes a HTTP 301 (permanent) redirect after the view finishes processing. If a
    value is returned, it is ignored. Allows for the view url to be callable so the
    reverse() lookup can be used.

    @permanent_redirect('/another-url/')
    def redirect_view(request):
        ...

    @redirect(lambda: reverse('some_viewname'))
    def do_redirect(request):
        ...

    """
    def outer(f):
        @wraps(f)
        def inner(request, *args, **kwargs):
            f(request, *args, **kwargs)
            return HttpResponsePermanentRedirect(url if not callable(url) else url())
        return inner
    return outer

#@permanent_redirect('/finance/students/')
def f_student_report(request, pago_id):
    
    pago = Pago.objects.get(pk=pago_id) #get_object_or_404
    student = pago.alumno
    student_services = student.suscript_services() #servicios suscriptos-no muestra pagos unicos realizados
    fecha = date.today()
    comentarios = pago.comentarios

    items = ItemPago.objects.filter(pago=pago.id)

    fname = '%s_%d-%d-%d' % (student.last_name, fecha.day, fecha.month, fecha.year)
    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename=%s.pdf' % fname

    result = generate_pdf('finance/f_student_report_improved.html', file_object=resp,
                 context={ 'student': student, 'services': student_services,
                         'items': items,
                 'pago': pago, 'fecha': fecha, 'comentarios': comentarios,
                 })

    return result





#def write_pdf(template_src, context_dict):
    #template = get_template(template_src)
    #context = Context(context_dict)
    #html  = template.render(context)
    #result = StringIO.StringIO()
    #pdf = pisa.pisaDocument(StringIO.StringIO(
        #html.encode("ISO-8859-1")), result)
    #if not pdf.err:
        #return http.HttpResponse(result.getvalue(), \
             #mimetype='application/pdf')
    #return http.HttpResponse("Error creando el pdf %s" % cgi.escape(html))
