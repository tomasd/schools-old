from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from nose.tools import eq_
from schools.lectors.models import Lector, Contract

class LectorTest(TestCase):
    fixtures = ['test_users', 'test_lectors']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        response = self.client.get(reverse('lectors'))
        self.assertEquals(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('lector-create'))
        self.assertEqual(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('lector-create'),
                dict(first_name='xxx', last_name='xxx'))
        lector = Lector.objects.latest('created')
        self.assertRedirects(response, lector.get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(reverse('lector-detail', kwargs={'object_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testUpdate_post(self):
        response = self.client.post(reverse('lector-detail', kwargs={'object_id':'1'}),
                dict(first_name='xxx', last_name='xxx'))
        self.assertRedirects(response, Lector.objects.get(pk=1).get_absolute_url())
        

class ContractTest(TestCase):
    fixtures = ['test_users', 'test_lectors']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testContractList(self):
        response = self.client.get(Lector.objects.get(pk=1).contracts_url())
        eq_(200, response.status_code)
        
    def testCreateContract(self):
        response = self.client.post(Lector.objects.get(pk=1).contracts_url(),
                    {'contract_number':'1', 'hour_rate':'500',
                     'start':'2008-01-01', 'end':'2008-01-01', })
        self.assertRedirects(response, Contract.objects.latest('created').get_absolute_url())
        
    def testUpdateContract(self):
        contract = Contract.objects.get(pk=1)
        eq_(1, contract.hourrate_set.count())
        
        response = self.client.get(contract.get_absolute_url())
        eq_(200, response.status_code)
        
        response = self.client.post(contract.get_absolute_url(),
                                    
                    {'contract_number':'1', 'hour_rate':'500',
                     'start':'2008-01-01', 'end':'2008-01-01',
                     'hourrate_set-TOTAL_FORMS':'3', 'hourrate_set-INITIAL_FORMS':'1', 
                     'hourrate_set-0-id':'1', 'hourrate_set-0-contract':'1', 'hourrate_set-0-course': '1', 'hourrate_set-0-hour_rate': '300',
                     'hourrate_set-1-contract':'1', 'hourrate_set-1-course': '1', 'hourrate_set-1-hour_rate': '300',
                     })
        self.assertRedirects(response, contract.get_absolute_url())
        
        eq_(2, contract.hourrate_set.count())
        
