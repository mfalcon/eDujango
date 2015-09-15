import datetime
from django.test import TestCase
from finance.models import *

'''
class AlumnoTestCase(TestCase):
    fixtures = ['cc_testdata.json']
    
    def setUp(self):
        super(AlumnoTestCase, self).setUp()
        self.alumno_1 = Alumno.objects.get(pk=1)
        self.alumno_2 = Alumno.objects.get(pk=2)

    def test_get_deuda(self):
        self.assertTrue(sum(self.alumno_1.get_deuda()), 885)

     
class CuotaTestCase(TestCase):
    fixtures = ['childcare_views_testdata.json']
    
    def setUp(self):
        super(CuotaTestCase, self).setUp()
        self.cuota_1 = Cuota.objects.get(pk=1)
        self.cuota_2 = Cuota.objects.get(pk=2)
        self.cuota_3 = Cuota.objects.get(pk=3)

    def test_pagar_cuota(self):
        self.assertEqual(self.cuota_1.pagar_cuota(385), 0)
        self.assertEqual(self.cuota_2.pagar_cuota(700), 200)
        self.assertEqual(self.cuota_3.pagar_cuota(100), 0)
        # sacar pagar_cuota de models
        self.assertEqual(self.cuota_1.deuda, 0) #no hay que hacer un save?
        self.assertEqual(self.cuota_2.deuda, 0)
        self.assertEqual(self.cuota_3.deuda, 700)
'''
