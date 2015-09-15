import datetime
import pdb
from django.test import TestCase

from finance.models import *
from efinance.models import *
from students.models import *

class UtilsTestCase(TestCase):
    fixtures = ['students_testdata.json']

    def setUp(self):
        super(UtilsTestCase, self).setUp()
        #self.cuota_1 = Cuota.objects.get(pk=1)
        #self.cuota_2 = Cuota.objects.get(pk=2)
        #self.cuota_3 = Cuota.objects.get(pk=3)
        #self.unico_pago_1 = UnicoPago.objects.get(pk=1)
        self.alumno_1 = Alumno.objects.get(pk=1)
        self.alumno_2 = Alumno.objects.get(pk=2)
        #self.empleado_1 = Empleado.objects.get(pk=1)
        #self.empleado_2 = Empleado.objects.get(pk=2)
    
    def test_pago_cuota(self):
        self.assertEqual(self.alumno_1.id, 1)
    
    def test_pago_sueldo(self):
        self.assertEqual(self.alumno_1.id, 1)    
    
    def test_gen_cuotas(self):
        self.assertEqual(self.alumno_1.id, 1)
    
    def test_gastos(self):
        self.assertEqual(self.alumno_1.id, 1) 

    def test_cashflow(self):
        self.assertEqual(self.alumno_1.id, 1)
    
    def test_pago_unico(self):
        self.assertEqual(self.alumno_1.id, 1) 
    
    def test_deuda_alumno(self):
        self.assertEqual(self.alumno_1.id, 1)
    
    def test_deuda_empleado(self):
        self.assertEqual(self.alumno_1.id, 1)     
    
    def test_monto_cuota(self):
        self.assertEqual(self.alumno_1.id, 1)     
    '''    
    def test_realizar_pago(self):
        self.assertEqual(realizar_pago(385,1), 0)
        self.assertEqual(realizar_pago(350,2), 0)

    def test_pagar_cuota(self):
        self.assertEqual(pagar_cuota(self.cuota_1.id, 385), 0)
        self.assertEqual(pagar_cuota(self.cuota_2.id, 700), 200)
        #self.assertEqual(pagar_cuota(self.cuota_3.id, 100), 0)
        
        self.setUp()

        self.assertEqual(self.cuota_1.deuda, 0)
        self.assertEqual(self.cuota_2.deuda, 0)
        #self.assertEqual(self.cuota_3.deuda, 700)
    
        
    def test_pagar_pu(self):
        self.assertEqual(pagar_pu(self.unico_pago_1.id, 500), 0)
        
        pu = UnicoPago.objects.get(pk=1)
        self.assertEqual(pu.deuda, 0)
    
        
    def test_pago_sueldo(self):
        #la que se usa en views
        #veronica monini cobra 6543 mensuales
        pago_sueldo(700, self.empleado_1.id)
        pago_sueldo(3200, self.empleado_2.id)
        
        self.setUp()
        
        self.assertEqual(self.empleado_1.get_deuda(), 1000)
        self.assertEqual(self.empleado_2.get_deuda(), 0)
        
    def test_pagar_sueldo(self):
        #un sueldo en particular
        pass
'''
        
        
    
