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
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.management import call_command
from tenant_schemas.utils import tenant_context
from django.views.generic.edit import FormView
from django.contrib.sites.models import Site
from django.conf import settings

from efinance.forms import PagoSueldoForm, GastoForm, DemoForm
from efinance.utils import generar_sueldos, pago_sueldo
from efinance.models import Gasto, Empleado, PagoSueldo, Sueldo, Client
from finance.models import Pago, UnicoPago, Cuota, CustomUser

from datetime import date
from dateutil.relativedelta import *
import datetime

import pdb


#There are three accounting reports that every business owner should understand. Profit-Loss, Balance Sheet, Statement of Cash Flows. Most small business people that I have met only look at the Profit-Loss (P&L) and do not look at the other two. They are the three legs of a stool. The P&L tells you how much money you made (or lost), the Balance Sheet tells you what the balances are on your accounts (bank balances, monies owed to you and monies you owe to others), and the Statement of Cash Flows tells you where and how the Balance Sheet changed and where the money moved to.
#If you are C level at your company, spend at least an hour a month understanding these three reports. If you don't understand something ask your accountant or Google. As the OP says, there are more than just employees jobs riding on these reports (or what they represent); their families are also depending on good numbers. Sometimes the reports are not good news - they key is not to fool yourself, but to understand the truth. If you understand the truth you can make better decisions. If you do not understand the truth, it is very hard to make a good decision.
#Some days you are making money, but you have to wait for accounts receivable to get paid. Some days you have a bunch of money in the bank because of new funding, or a customer pre-paid, or you haven't taken care of all the payables yet. Just don't lie to yourself, and don't get lied to.
#It is not that hard to understand the three reports; they are basic arithmetic and counting - the key is to just do it. Personally, I look at it every week after doing payroll. You can choose your own schedule, just choose one and look at all three reports. Even if you only do it quarterly, you will at least know what is going on.

class DemoView(FormView):
    template_name = 'demo.html'
    form_class = DemoForm

    def get_success_url(self):
        return 'http://'+self.url+'/jardin/'

    def form_valid(self, form):
        nombre = (form.cleaned_data.get('nombre')).replace(' ','').lower()
        self.url = nombre + '.' + settings.SITE_URL
        tenant = Client(domain_url=self.url,
                        schema_name=nombre,
                        nombre=nombre,
                        paid_until='2014-12-05',
                        on_trial=True)
        tenant.save()
        usuarioAdmin = form.cleaned_data.get('dni')
        passwordAdmin = form.cleaned_data.get('password1')
        datosPrueba = form.cleaned_data.get('datosPrueba')

        with tenant_context(tenant):
            CustomUser.objects.create_superuser(num_doc=usuarioAdmin, password=passwordAdmin)
            s = Site(domain=self.url,name=nombre)
            s.save()
            
            if datosPrueba:
                call_command('load_schema_data', 'sala.json', schema_name=nombre, verbosity=0,)
        

        return super(DemoView, self).form_valid(form)


@login_required
def empleados(request):
    empleados = Empleado.objects.all()

    context = {
        'empleados' : empleados,
    }
    return render_to_response(
        'efinance/f_empleados.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def gastos(request):
    gastos = Gasto.objects.all()

    context = {
        'gastos' : gastos,
    }
    return render_to_response(
        'efinance/f_gastos.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def f_gasto_info(request, gasto_id):
    g = Gasto.objects.get(id=gasto_id)

    context = {
        'g': g,
    }
    return render_to_response(
        'efinance/f_detalle_gasto.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def nuevo_gasto(request):
    if request.method == 'POST':
        form = GastoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('f_gastos'))
    else:
        form = GastoForm()

    context = {
        'form': form,
    }
    return render_to_response(
        'efinance/f_nuevo_gasto.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def modificar_gasto(request,gasto_id):
    gasto = Gasto.objects.get(pk=gasto_id)
    dictionary = model_to_dict(gasto, fields=[], exclude=[])
    if request.method == 'POST':
        form = GastoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('f_gastos'))
    else:
        form = GastoForm(dictionary)

    context = {
        'form': form,
    }
    return render_to_response(
        'efinance/e_modificar_gasto.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def sueldos_mensuales(request):
    ya_generados = generar_sueldos()

    context = {
        'ya_generados': ya_generados,
    }
    return render_to_response(
        'efinance/f_sueldos.html',
        context,
        context_instance = RequestContext(request),
    )

@login_required
def pagar_sueldo(request, emp_id):
    empleado = Empleado.objects.get(pk=emp_id)

    if request.method == 'POST':
        form = PagoSueldoForm(empleado=empleado, data=request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.empleado = empleado
            pago_sueldo(pago.abona, empleado.id)
            pago.save()
            return HttpResponseRedirect(reverse('f_empleado_info', args=[empleado.id]))
            #return HttpResponseRedirect(reverse('f_student_report', args=[payment.id]))

    else:
        form = PagoSueldoForm(empleado=empleado)

    context = {
        'form': form, 'empleado': empleado,
    }
    return render_to_response(
        'efinance/f_pagar_sueldo.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def modificar_pago_sueldo(request, pago_id):
    pago = PagoSueldo.objects.get(pk=pago_id)
    empleado = pago.empleado
    dictionary = model_to_dict(pago, fields=[], exclude=[])

    if request.method == 'POST':
        form = PagoSueldoForm(empleado=empleado, data=request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.empleado = empleado
            pago_sueldo(pago.abona, empleado.id)
            #mod_sueldo()
            pago.save()
            return HttpResponseRedirect(reverse('f_empleado_info', args=[empleado.id]))
            #return HttpResponseRedirect(reverse('f_student_report', args=[payment.id]))

    else:
        form = PagoSueldoForm(dictionary, empleado=empleado)

    context = {
        'form': form, 'empleado': empleado,
    }
    return render_to_response(
        'efinance/f_modificar_pago_sueldo.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def f_empleado_info(request, emp_id):
    empleado = Empleado.objects.get(pk=emp_id)
    #emp_deuda = empleado.get_deuda()
    #emp_ult_pagos = empleado.last_payments(5)

    context = {
        'empleado' : empleado,
        #'st_debt' : st_debt,
        #'st_last_payments' : st_last_payments,
    }
    return render_to_response(
        'efinance/f_empleado_info.html',
         context,
         context_instance = RequestContext(request),
    )

#TODO usar una funcion para la lista_mov, todos los cashflow se calculan igual
@login_required
def f_cashflow_diario(request):
    hoy = date.today()
    pago_cuotas = [(p, 'ingreso') for p in Pago.objects.filter(fecha=hoy)] # abona
    pagos_unicos = [(u, 'ingreso_unico') for u in UnicoPago.objects.filter(fecha=hoy)]
    gastos = [(g, 'gasto') for g in Gasto.objects.filter(fecha=hoy)] # importe
    sueldos =[(s, 'sueldo') for s in PagoSueldo.objects.filter(fecha=hoy)] #abona
    lista_mov = pago_cuotas + pagos_unicos + gastos + sueldos

    ingresos = sum([p[0].abona for p in pago_cuotas]) + sum([pu[0].importe for pu in pagos_unicos])
    gastos = sum([g[0].importe for g in gastos]) + sum([s[0].abona for s in sueldos])

    context = {
        'movimientos' : lista_mov, 'ingresos': ingresos, 'gastos': gastos,
    }
    return render_to_response(
        'jardin/cashflow_diario.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def f_cashflow_semanal(request):
    today = date.today()
    weekday = date.today().isoweekday() # Monday 0, Sunday 6
    first_day_of_week = today+relativedelta(days=-(weekday+1)) #me posiciono en el lunes de la semana actual
    dates_list = []
    for d in range(7):
        dates_list.append(first_day_of_week+relativedelta(days=+d)) # FIX MEesta guardando sabado y domingo de la sem pasada

    pago_cuotas = [(p, 'ingreso') for p in Pago.objects.filter(fecha__range=(dates_list[0],dates_list[6]))] # abona
    pagos_unicos = [(u, 'ingreso_unico') for u in UnicoPago.objects.filter(fecha__range=(dates_list[0],dates_list[6]))]
    gastos = [(g, 'gasto') for g in Gasto.objects.filter(fecha__range=(dates_list[0],dates_list[6]))] # importe
    sueldos =[(s, 'sueldo') for s in PagoSueldo.objects.filter(fecha__range=(dates_list[0],dates_list[6]))] #abona
    lista_mov = pago_cuotas + pagos_unicos + gastos + sueldos

    ingresos = sum([p[0].abona for p in pago_cuotas]) + sum([pu[0].importe for pu in pagos_unicos])
    gastos = sum([g[0].importe for g in gastos]) + sum([s[0].abona for s in sueldos])

    balance = ingresos - gastos

    context = {
        'movimientos' : lista_mov, 'ingresos': ingresos, 'gastos': gastos,
        'balance': balance,
    }
    return render_to_response(
        'jardin/cashflow_semanal.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def f_cashflow_mensual(request):

    mes_actual = date.today().month
    #TODO: no diferenciar entre pago cuotas y pago unicos al mostrarlo en el template
    pago_cuotas = [(p, 'ingreso') for p in Pago.objects.filter(fecha__month=mes_actual)] # abona
    pagos_unicos = [(u, 'ingreso_unico') for u in UnicoPago.objects.filter(fecha__month=mes_actual)]
    gastos = [(g, 'gasto') for g in Gasto.objects.filter(fecha__month=mes_actual)] # importe
    sueldos =[(s, 'sueldo') for s in PagoSueldo.objects.filter(fecha__month=mes_actual)] #abona
    lista_mov = pago_cuotas + pagos_unicos + gastos + sueldos

    ingresos = sum([p[0].abona for p in pago_cuotas]) + sum([pu[0].importe for pu in pagos_unicos])
    gastos = sum([g[0].importe for g in gastos]) + sum([s[0].abona for s in sueldos])

    #deudas TODO: crear una seccion aparte
    deudas_cuotas = sum([c.deuda for c in Cuota.objects.filter(paga=False)])
    deudas_unicos = sum([u.deuda for u in UnicoPago.objects.filter(paga=False)])
    deudas_sueldos = sum([s.deuda for s in Sueldo.objects.filter(pago=False)])
    deudas_gastos = sum([g.importe for g in Gasto.objects.filter(pago=False)])

    context = {
        'movimientos' : lista_mov, 'ingresos': ingresos, 'gastos': gastos,
        'dcuotas': deudas_cuotas, 'dunicos': deudas_unicos,
        'dsueldos': deudas_sueldos, 'dgastos': deudas_gastos,
    }
    return render_to_response(
        'jardin/cashflow_mensual.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def f_cashflow_anual(request):

    anio_actual = date.today().year

    pago_cuotas = [(p, 'ingreso') for p in Pago.objects.filter(fecha__year=anio_actual)] # abona
    pagos_unicos = [(u, 'ingreso_unico') for u in UnicoPago.objects.filter(fecha__year=anio_actual)]
    gastos = [(g, 'gasto') for g in Gasto.objects.filter(fecha__year=anio_actual)] # importe
    sueldos =[(s, 'sueldo') for s in PagoSueldo.objects.filter(fecha__year=anio_actual)] #abona
    lista_mov = pago_cuotas + pagos_unicos + gastos + sueldos

    ingresos = sum([p[0].abona for p in pago_cuotas]) + sum([pu[0].importe for pu in pagos_unicos])
    gastos = sum([g[0].importe for g in gastos]) + sum([s[0].abona for s in sueldos])

    context = {
        'movimientos' : lista_mov, 'ingresos': ingresos, 'gastos': gastos,
    }
    return render_to_response(
        'jardin/cashflow_anual.html',
         context,
         context_instance = RequestContext(request),
    )


@login_required
def f_estado_financiero(request):
    deudas_cuotas = sum([c.deuda for c in Cuota.objects.filter(paga=False)])
    deudas_unicos = sum([u.deuda for u in UnicoPago.objects.filter(paga=False)])
    deudas_sueldos = sum([s.deuda for s in Sueldo.objects.filter(pago=False)])
    deudas_gastos = sum([g.importe for g in Gasto.objects.filter(pago=False)])

    context = {
        'dcuotas': deudas_cuotas, 'dunicos': deudas_unicos,
        'dsueldos': deudas_sueldos, 'dgastos': deudas_gastos,
    }
    return render_to_response(
        'jardin/estado_financiero.html',
         context,
         context_instance = RequestContext(request),
    )
