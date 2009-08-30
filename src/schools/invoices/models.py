from django.db import models
from django.db.models import permalink

# Create your models here.
class Invoice(models.Model):
    from schools.companies.models import Company
    company = models.ForeignKey(Company)
    start = models.DateField()
    end = models.DateField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        format = '%d.%m.%Y'
        return '%s (%s-%s)' % (self.company, self.start.strftime(format), self.end.strftime(format))
    
    @permalink
    def get_absolute_url(self):
        return ('invoice-detail', None, {'object_id':str(self.pk)})
    
    @permalink
    def get_lesson_attendees_url(self):
        return ('invoice-lesson-attendees', None, {'object_id':str(self.pk)})
    
    
def create_invoice(company, start, end):
    '''
        Create invoice for the company for specified time, when there
        is something to be invoiced.
    '''
    from schools.courses.models import LessonAttendee
    attendees = LessonAttendee.objects.for_invoice(company, start, end)
    if attendees:
        invoice = Invoice(company=company, start=start, end=end)
        invoice.save()
        invoice.lessonattendee_set = attendees
        
        # mark lessons as invoiced
        lessons = [a.attendance_list.lesson for a in attendees]
        for lesson in lessons:
            lesson.invoiced = True
            lesson.save()
        return invoice
    
def create_invoices(start, end): 
    '''
        Create invoice for each company when something should be invoiced.
    '''
    from schools.companies.models import Company
    invoices = []
    for company in Company.objects.all():
        invoice = create_invoice(company, start, end)
        invoices.append(invoice)
    return filter(None, invoices)