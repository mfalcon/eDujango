from finance.settings import SIN_SUELDO
from efinance.models import Sueldo, Empleado

from datetime import date

import pdb

def generar_sueldos():
    '''
    se podria pasar como parametro un "payment date" para generar  sueldos de
    meses determinados.
    devuelve true si ya se habian generado y false sino.
    '''
    #Analiza si debe crear los sueldos del mes actual. 
    today = date.today()
    today_tuple = (today.year, today.month)
    # hacer un get y no un filter(ahorro de queries)
    s = Sueldo.objects.filter(fecha__month=today.month, fecha__year=today.year) 
    #s = []
    if not s and today.month not in SIN_SUELDO:
        empleados = Empleado.objects.all()
        for empleado in empleados:
            #pdb.set_trace()
            sueldo = empleado.get_sueldo_bruto()
            if sueldo:
                s = Sueldo(empleado=empleado, importe=sueldo, deuda=sueldo, fecha=today) 
                s.save()
        return False
    return True

def pago_sueldo(monto, emp_id):
    empleado = Empleado.objects.get(pk=emp_id)
    deuda = empleado.get_deuda()
    sueldos_no_pagos = Sueldo.objects.filter(empleado=empleado, pago=False)
    for s in sueldos_no_pagos: # cuotas al reves, primer elemento cuota mas antigua
        if monto != 0:
            monto = pagar_sueldo(s.id, monto)
        else:
            break
    return 0

def pagar_sueldo(sueldo_id, monto):
    s = Sueldo.objects.get(pk=sueldo_id)
    ''' regresa el monto sobrante'''
    if monto < s.deuda:
        #c.deuda = F('deuda') - monto # ver bien F
        s.deuda -= monto
        s.save()
    elif monto == s.deuda:
        s.deuda = 0
        s.pago = True
        s.save()
    else: # monto > deuda (sobra)
        monto -= s.deuda
        s.deuda = 0
        s.pago = True
        s.save()
        return monto
    return 0
