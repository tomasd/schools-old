from datetime import date
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
from django.utils.datetime_safe import datetime
from nose.tools import eq_, ok_
from schools.courses.models import Course, CourseMember, Lesson, AttendanceList, \
    ExpenseGroup
from schools.lectors.models import lector_price, Lector
from schools.students.models import Student

class CourseTest(TestCase):
    fixtures = ['test_courses', 'test_users']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()

    def testList(self):
        response = self.client.get(reverse('courses'))
        eq_(200, response.status_code)
        
    def testCreate(self):
        response = self.client.get(reverse('course-create'))
        eq_(200, response.status_code)
        
    def testCreate_post(self):
        response = self.client.post(reverse('course-create'), {'slug':'new_slug', 'responsible':'1', 'lector':'1'})
        self.assertRedirects(response, reverse('course-detail', kwargs={'slug':'new_slug'}))
        
class CourseMemberTest(TestCase):
    fixtures = ['test_courses', 'test_users']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        course = Course.objects.get(pk=1)
        response = self.client.get(course.course_members_url())
        eq_(200, response.status_code)
        
    def testCreate_post_create_expense_group(self):
        response = self.client.post(reverse('course-members', kwargs={'slug':'1234'}),
                    {'student':'1', 'start':'2008-01-01', 'price':'500'})
        course_member = CourseMember.objects.latest('created')
        self.assertRedirects(response, course_member.get_absolute_url())
        
        eq_(1, course_member.expense_group.expensegroupprice_set.count())
        eq_(500, course_member.expense_group.expensegroupprice_set.get().price)
        eq_(course_member.start, course_member.expense_group.expensegroupprice_set.get().start)
        
    def testCreate_post(self):
        response = self.client.post(reverse('course-members', kwargs={'slug':'1234'}),
                    {'student':'1', 'start':'2008-01-01', 'expense_group':'1'})
        self.assertRedirects(response, CourseMember.objects.latest('created').get_absolute_url())
        
    def testUpdate(self):
        course = Course.objects.get(pk=1)
        member = CourseMember(course=Course.objects.get(pk=1),
                              student=Student.objects.get(pk=1),
                              start='2008-01-01',
                              expense_group=course.expensegroup_set.get(pk=1))
        member.save()
        response = self.client.get(member.get_absolute_url())
        eq_(200, response.status_code)
        
        response = self.client.post(member.get_absolute_url(), {
                    'student':'1', 'start':'2008-01-01', 'end':'2008-12-31', 'expense_group':'1',
                    'testresult_set-TOTAL_FORMS':'1', 'testresult_set-INITIAL_FORMS':'0',
                    'coursememberassessment_set-TOTAL_FORMS':'1', 'coursememberassessment_set-INITIAL_FORMS':'0',
                    'testresult_set-0-test':'1', 'testresult_set-0-points':'100', 'testresult_set-0-date':'2008-01-01',
                    'coursememberassessment_set-0-description':'xxx', 'coursememberassessment_set-0-date':'2008-01-01',
                    })
        self.assertRedirects(response, member.get_absolute_url())
        member = CourseMember.objects.get(pk=member.pk)
        ok_(member.end is not None)
        
        eq_(1, member.testresult_set.count())
        eq_(1, member.coursememberassessment_set.count())
        
class LessonTest(TestCase):
    fixtures = ['test_courses', 'test_users']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()
        
    def testList(self):
        course = Course.objects.get(pk=1)
        response = self.client.get(course.lesson_set.get().get_absolute_url())
        eq_(200, response.status_code)
        
    def testCreate_post(self):
        course = Course.objects.get(pk=1)
        count = course.lesson_set.count()
        response = self.client.post(reverse('course-lessons', kwargs={'slug':course.slug}),
                                    {'classroom':'1', 'start_0':'2008-01-01', 'end_0':'2008-01-01',
                                     'start_1':'01:00','end_1':'02:00'})
        self.assertRedirects(response, Lesson.objects.latest('created').get_absolute_url())
        eq_(count + 1, course.lesson_set.count())
    
    def testUpdate_post(self):
        response = self.client.post(Lesson.objects.get(pk=1).get_absolute_url()) 
        eq_(200, response.status_code)
        
        response = self.client.post(Lesson.objects.get(pk=1).get_absolute_url(),
                                    {'classroom':'1', 'start_0':'2008-01-01', 'end_0':'2008-01-01',
                                     'start_1':'01:00','end_1':'02:00'})
        self.assertRedirects(response, Lesson.objects.get(pk=1).get_absolute_url())
        
    def testAttendaceList(self):
        lesson = Lesson.objects.get(pk=1)
        
        try:
            # delete existing attendance list to simulate that one is created,
            # when accessing it
            lesson.attendancelist.delete()
        except AttendanceList.DoesNotExist: #@UndefinedVariable
            pass
        
        response = self.client.get(lesson.get_attendance_list_url())
        eq_(200, response.status_code)
        
        data = {'classroom':'1', 'start_0':'2008-01-01', 'start_1':'00:00', 'end_0':'2008-01-01', 'end_1':'01:00',
                     'lector':'1', 'course_members':['1','2']}
        
        response = self.client.post(lesson.get_attendance_list_url(), data)
        self.assertRedirects(response, lesson.get_attendance_list_url())
        
        lesson = Lesson.objects.get(pk=1)
        eq_(lector_price(Lector.objects.get(pk=1), Course.objects.get(pk=1), datetime(2008, 1, 1), datetime(2008, 1, 1, 1)),
            lesson.attendancelist.lector_price)
        eq_([True,True,False], [a.present for a in lesson.attendancelist.lessonattendee_set.all()])
        
        data['course_members'] = ['1', '3']
        response = self.client.post(lesson.get_attendance_list_url(), data)
        eq_([True,False,True], [a.present for a in lesson.attendancelist.lessonattendee_set.all()])

class ExpenseGroupTest(TestCase):
    fixtures = ['test_courses', 'test_users']
    
    def login(self, user='tomas'):
        password = {'tomas':'tomas'}[user]
        self.client.login(username=user, password=password)
    
    def setUp(self):
        self.login()

    def testList(self):
        course = Course.objects.get(pk=1)
        response = self.client.get(course.course_expense_groups_url())
        eq_(200, response.status_code)
        
    def testCreate(self):
        course = Course.objects.get(pk=1)
        response = self.client.post(course.course_expense_groups_url(),
                    {'name':'xxx', 'price':'30', 'start':'2008-01-01'})
        
        expense_group = ExpenseGroup.objects.latest('created')
        self.assertRedirects(response, expense_group.get_absolute_url())
        eq_('xxx', expense_group.name)
        eq_(1, expense_group.expensegroupprice_set.count())
        eq_(30, expense_group.expensegroupprice_set.get().price)
        eq_(date(2008, 1, 1), expense_group.expensegroupprice_set.get().start)
        eq_(None, expense_group.expensegroupprice_set.get().end)
        
    def testUpdate(self):
        expense_group = ExpenseGroup.objects.get(pk=1)
        response = self.client.get(expense_group.get_absolute_url())
        eq_(200, response.status_code)
        
        response = self.client.post(expense_group.get_absolute_url(),
                        {'name':'xxx',
                         'expensegroupprice_set-0-start':'2008-01-01',
                         'expensegroupprice_set-0-price':'30',
                         'expensegroupprice_set-TOTAL_FORMS':'2',
                         'expensegroupprice_set-INITIAL_FORMS':'0'})
        self.assertRedirects(response, expense_group.get_absolute_url())
