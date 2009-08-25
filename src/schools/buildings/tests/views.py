from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from schools.buildings.models import Building, Classroom, BuildingMonthExpense

class BuildingTest(TestCase):
    fixtures = ['test_users', 'test_buildings']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        response = self.client.get(reverse('buildings'))
        self.assertEquals(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('building-create'))
        self.assertEqual(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('building-create'),
                dict(name='xxx', street='xxx', postal='xxx', town='xxx',))
        building = Building.objects.latest('created')
        self.assertRedirects(response, building.get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(reverse('building-detail', kwargs={'object_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testUpdate_post(self):
        response = self.client.post(reverse('building-detail', kwargs={'object_id':'1'}),
                    dict(name='xxx', street='xxx', postal='xxx', town='xxx',))
        self.assertRedirects(response, Building.objects.get(pk=1).get_absolute_url())
        
class ClassroomTest(TestCase):
    fixtures = ['test_users', 'test_buildings']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        response = self.client.get(reverse('classrooms', kwargs={'building_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('classroom-create', kwargs={'building_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('classroom-create', kwargs={'building_id':'1'}),
                       {'name':'xxx'})
        self.assertRedirects(response, Classroom.objects.latest('created').get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(reverse('classroom-detail', kwargs={'building_id':'1', 'classroom_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testUpdate_post(self):
        response = self.client.post(reverse('classroom-detail', kwargs={'building_id':'1', 'classroom_id':'1'}),
                        {'name':'xxx'})
        self.assertRedirects(response, Classroom.objects.get(pk=1).get_absolute_url())
        
class BuildingMonthExpenseTest(TestCase):
    fixtures = ['test_users', 'test_buildings']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self): 
        response = self.client.get(reverse('building-expenses', kwargs={'building_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('building-expense-create', kwargs={'building_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('building-expense-create', kwargs={'building_id':'1'}),
                       {'start':'2008-01-01', 'end':'2008-12-31', 'price':'500'})
        self.assertRedirects(response, BuildingMonthExpense.objects.latest('created').get_absolute_url())
        
    def testUpdate(self):
        response = self.client.get(reverse('building-expense-detail', kwargs={'building_id':'1', 'building_expense_id':'1'}))
        self.assertEquals(200, response.status_code)
        
    def testUpdate_post(self):
        response = self.client.post(reverse('building-expense-detail', kwargs={'building_id':'1', 'building_expense_id':'1'}),
                        {'start':'2008-01-01', 'end':'2008-12-31', 'price':'500'})
        self.assertRedirects(response, BuildingMonthExpense.objects.get(pk=1).get_absolute_url())
