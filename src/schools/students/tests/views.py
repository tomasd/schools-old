from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from schools.students.models import Student

class StudentTest(TestCase):
    fixtures = ['test_users', 'test_students']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        response = self.client.get(reverse('students'))
        self.assertEquals(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('student-create'))
        self.assertEqual(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('student-create'),
                dict(first_name='xxx', last_name='xxx'))
        student = Student.objects.latest('created')
        self.assertRedirects(response, student.get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(reverse('student-detail', kwargs={'object_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testUpdate_post(self):
        response = self.client.post(reverse('student-detail', kwargs={'object_id':'1'}),
                dict(first_name='xxx', last_name='xxx'))
        self.assertRedirects(response, Student.objects.get(pk=1).get_absolute_url())
        
