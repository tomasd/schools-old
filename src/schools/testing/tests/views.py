from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from nose.tools import eq_
from schools.testing.models import Test

class TestTest(TestCase):
    fixtures = ['test_users', 'test_tests']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        response = self.client.get(reverse('tests'))
        eq_(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('test-create'))
        eq_(200, response.status_code)
        
        response = self.client.post(reverse('test-create'), {'name':'xxx', 'description':'xxx', 'max_points':'100'})
        self.assertRedirects(response, Test.objects.latest('created').get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(Test.objects.get(pk=1).get_absolute_url())
        eq_(200, response.status_code)
        
        response = self.client.post(reverse('test-create'), {'name':'xxx', 'description':'xxx', 'max_points':'100'})
        self.assertRedirects(response, Test.objects.latest('created').get_absolute_url())
