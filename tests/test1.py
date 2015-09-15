import datetime
import pdb
from django.test import TestCase

from childcare.models import *
from childcare.utils import * 

class UtilsTestCase(TestCase):
    fixtures = ['childcare_views_testdata.json']

    def setUp(self):
        super(UtilsTestCase, self).setUp()
        self.cuota_1 = Cuota.objects.get(pk=1)
        self.cuota_2 = Cuota.objects.get(pk=2)
        self.cuota_3 = Cuota.objects.get(pk=3)
        self.unico_pago_1 = UnicoPago.objects.get(pk=1)
    
    def test_realizar_pago(self):
        pass
        #self.assertEqual(realizar_pago(385,1), 0)
        #self.assertEqual(realizar_pago(350,1), 0)

    def test_pagar_cuota(self):
        self.assertEqual(pagar_cuota(self.cuota_1.id, 385), 0)
        self.assertEqual(pagar_cuota(self.cuota_2.id, 700), 200)
        self.assertEqual(pagar_cuota(self.cuota_3.id, 100), 0)
        
        self.setUp()

        self.assertEqual(self.cuota_1.deuda, 0)
        self.assertEqual(self.cuota_2.deuda, 0)
        self.assertEqual(self.cuota_3.deuda, 700)
        
    def test_pagar_pu(self):
        self.assertEqual(pagar_pu(self.unico_pago_1.id, 500), 0)
        
        pu = UnicoPago.objects.get(pk=1)
        self.assertEqual(pu.deuda, 0)
        
    
