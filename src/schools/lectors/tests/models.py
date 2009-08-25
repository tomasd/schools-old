from datetime import datetime
from decimal import Decimal
from django.test.testcases import TestCase
from nose.tools import eq_
from schools.courses.models import Course
from schools.lectors.models import lector_price, Lector

class PriceTest(TestCase):
    fixtures = ['test_lectors']
    
    def testLectorPrice(self):
        lector = Lector.objects.get(pk=1)
        course1 = Course.objects.get(pk=1)
        course2 = Course.objects.get(pk=2)
        
        # price from hour rate
        price = lector_price(lector, course1, datetime(2008,1,1,19), datetime(2008,1,1,20,30))
        eq_(Decimal(str(500*1.5)), price)
        
        # price from contract
        price = lector_price(lector, course2, datetime(2008,1,1,19), datetime(2008,1,1,20,30))
        eq_(Decimal(str(300*1.5)), price)
        
        # price from hour rate
        price = lector_price(lector, course1, datetime(2008,1,2,19), datetime(2008,1,3,20,30))
        eq_(Decimal(str(600*25.5)), price)
        
        # price from contract
        price = lector_price(lector, course2, datetime(2008,1,2,19), datetime(2008,1,3,20,30))
        eq_(Decimal(str(400*25.5)), price)
        
        