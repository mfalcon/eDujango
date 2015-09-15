import datetime
from django.test import TestCase

import pdb

class StudentsViewsTestCase(TestCase):
    fixtures = ['students_testdata.json']
    def test_index(self):
        resp = self.client.get('/students/')
        self.assertEqual(resp.status_code, 200)
    '''
    def test_list(self):
        resp = self.client.get('/childcare/students/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['students'][0].pk, 1)
    '''
    ''' 
    def test_student_info(self):
        resp = self.client.get('/childcare/students/info/1')
        self.assertEqual(resp.status_code, 301)
        pdb.set_trace()
        self.assertEqual(resp.context['student'].pk, 1)

        # Ensure that non-existent polls throw a 404.
        resp = self.client.get('/childcare/students/info/5')
        self.assertEqual(resp.status_code, 404)
    '''
    def test_monthly_payments(self):
        #resp = self.client.get('/childcare/finance/students/gen_payment/')
        a = 1

    def test_new_payment(self):
        pass
        
