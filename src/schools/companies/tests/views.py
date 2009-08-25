from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from schools.companies.models import Company

class CompanyTest(TestCase):
    fixtures = ['test_users', 'test_companies']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        response = self.client.get(reverse('companies'))
        self.assertEquals(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('company-create'))
        self.assertEqual(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('company-create'),
                dict(name='xxx'))
        company = Company.objects.latest('created')
        self.assertRedirects(response, company.get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(reverse('company-detail', kwargs={'object_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testUpdate_post(self):
        response = self.client.post(reverse('company-detail', kwargs={'object_id':'1'}),
                    dict(name='xxx', street='xxx', postal='xxx', town='xxx',))
        self.assertRedirects(response, Company.objects.get(pk=1).get_absolute_url())
        
