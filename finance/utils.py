from datetime import date

from django.db.models import F

from finance.settings import SIN_CUOTA
from finance.models import ServicioSuscripto, Cuota, Pago, UnicoPago
from students.models import Alumno


def pagar_cuota(cuota_id, monto):
    c = Cuota.objects.get(pk=cuota_id)
    ''' regresa el monto sobrante'''
    if monto < c.deuda:
        #c.deuda = F('deuda') - monto # ver bien F
        c.deuda -= monto
        c.save()
    elif monto == c.deuda:
        c.deuda = 0
        c.paga = True
        c.save()
    else: # monto > deuda (sobra)
        monto -= c.deuda
        c.deuda = 0
        c.paga = True
        c.save()
        return monto, c
    return 0, c


def pagar_pu(pu_id, monto):
    pu = UnicoPago.objects.get(pk=pu_id)
    ''' regresa el monto sobrante'''

    if monto < pu.deuda:
        #c.deuda = F('deuda') - monto # ver bien F
        pu.deuda -= monto
        pu.save()
    elif monto == pu.deuda:
        pu.deuda = 0
        pu.paga = True
        pu.save()
    else: # monto > deuda (sobra)
        monto -= pu.deuda
        pu.deuda = 0
        pu.paga = True
        pu.save()
        return monto, pu
    return 0, pu

#TODO: representar pagos de la forma: ['cuota 3/13(restan $x)', 'importe abonado']
#en realidad si lo quiero guardar en el model del pago, tendria que guardarlo como string o
#como un json al menos.
#FIXME: la solucion mas limpia deberia ser pasar como parametro de alguna forma no?
def rep_pagos(servicio, inst, monto_pagado):
    if servicio == 'cuota':
        if inst.paga:
            rep =  ['Cuota %d/%d' % (inst.fecha.month, inst.fecha.year),
                    monto_pagado]
        else:
            rep =  ['Cuota %d/%d(restan $%.2f)' % (inst.fecha.month, inst.fecha.year, inst.deuda),
                    monto_pagado]
    elif servicio == 'unico':
        if inst.paga:
            rep =  ['%s' % (inst.tipo.get_tipo_display()),
                    monto_pagado]
        else:
            rep =  ['%s (restan $%.2f)' % (inst.tipo.get_tipo_display(), inst.deuda),
                    monto_pagado]

    return rep


def realizar_pago(monto, st_id):
    '''
    Con el monto ingresado se encarga de cubrir pagos unicos/cuotas
    prioridad cuotas, si al realizar el pago cuota.deuda == 0 entonces
    cuota.paga = True
    el monto ya viene validado - es positivo y no mayor a la deuda
    devuelve el monto que deberia ser 0
    '''
    # TEST AND FIX
    alumno = Alumno.objects.get(pk=st_id)
    deuda_cuotas, deuda_unicos, cuotas_no_pagas, unicos_no_pagos = alumno.get_deuda(extra=True)
    cuotas_no_pagas.reverse()

    servicios_pagados = [] #servicios que esta pagando el cliente
    if monto == deuda_cuotas:
        for c in cuotas_no_pagas: # cuotas al reves, primer elemento cuota mas antigua
            if monto:
                monto_inicial = monto
                monto, c = pagar_cuota(c.id, monto)
                pago = monto_inicial - monto
                sv = rep_pagos('cuota',c, pago)
                servicios_pagados.append(sv)
            else:
                break
    #elif monto == deuda_unicos:
        #for pu in unicos_no_pagos: # cuotas al reves, primer elemento cuota mas antigua
            #if monto != 0:
                #monto = pagar_pu(pu.id, monto)
            #else:
                #break
    elif monto < deuda_cuotas:
        for c in cuotas_no_pagas: # cuotas al reves, primer elemento cuota mas antigua
            if monto:
                monto_inicial = monto
                monto, c = pagar_cuota(c.id, monto)
                pago = monto_inicial - monto
                sv = rep_pagos('cuota',c, pago)
                servicios_pagados.append(sv)
            else:
                break
    elif monto > deuda_cuotas:
        for c in cuotas_no_pagas: # cuotas al reves, primer elemento cuota mas antigua
            if monto:
                monto_inicial = monto
                monto, c = pagar_cuota(c.id, monto)
                pago = monto_inicial - monto
                sv = rep_pagos('cuota',c, pago)
                servicios_pagados.append(sv)
            else:
                break
        for pu in unicos_no_pagos: # cuotas al reves, primer elemento cuota mas antigua
            if monto:
                monto_inicial = monto
                monto, pu = pagar_pu(pu.id, monto)
                pago = monto_inicial - monto
                sv = rep_pagos('unico', pu, pago)
                servicios_pagados.append(sv)
            else:
                break


    return servicios_pagados


def generate_payments():
    '''
    se podria pasar como parametro un "payment date" para generar cuotas de
    meses determinados.
    devuelve true si ya se habian generado y false sino.
    '''
    amount = 0
    #Analiza si debe crear las cuotas del mes actual.
    today = date.today()
    today_tuple = (today.year, today.month)
    # hacer un get y no un filter(ahorro de queries)
    c = Cuota.objects.filter(fecha__month=today.month, fecha__year=today.year)
    if not c and today.month not in SIN_CUOTA:
        students = Alumno.objects.all()
        for student in students:
            services = ServicioSuscripto.objects.filter(alumno=student)
            for service in services:
                amount += service.importe
            c = Cuota(alumno=student, importe=amount, deuda=amount, fecha=today)
            c.save()
            amount = 0
        return False
    return True


