from django.test.testcases import TestCase
from schools.invoices.models import create_invoices
from datetime import date

class InvoiceGenerateTest(TestCase):
    fixtures=['testinvoices']
    
    def test(self):
        invoices = create_invoices(date(2008, 1, 1), date(2008, 1, 31))
        self.assertEquals(1, len(invoices))
        [invoice] = invoices
        
        self.assertEquals(2, invoice.lessonattendee_set.count())
