from datetime import datetime
from decimal import Decimal
from django.test.testcases import TestCase
from nose.tools import eq_
from schools.courses.models import CourseMember, course_member_price

class CourseMemberPrice(TestCase):
    fixtures = ['test_courses']
    
    def testCourseMemberPrice(self):
        course_member1 = CourseMember.objects.get(pk=1)
        course_member2 = CourseMember.objects.get(pk=2)
        course_member3 = CourseMember.objects.get(pk=3)
        
        price = course_member_price(course_member1, datetime(2008,1,1,19), datetime(2008,1,1,20,30))
        eq_(Decimal(str(60*1.5/2)), price)
        
        price = course_member_price(course_member1, datetime(2008,1,1,19), datetime(2008,1,1,20,30), [course_member1, course_member2, course_member3])
        eq_(Decimal(str(60*1.5/2)), price)