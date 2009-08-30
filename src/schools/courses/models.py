from decimal import Decimal
from django.db import models
from django.db.models import permalink
from django.db.models.query_utils import Q
from django.utils import dateformat

# Create your models here.
class Course(models.Model):
    from django.contrib.auth.models import User
    from schools.lectors.models import Lector
    slug = models.SlugField(unique=True)
    responsible = models.ForeignKey(User)
    lector = models.ForeignKey(Lector)
    
    name = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    def __unicode__(self):
        return self.slug
    
    @permalink
    def get_absolute_url(self):
        return ('course-detail', (), {'slug':self.slug})
    
    @permalink
    def course_members_url(self):
        return ('course-members', (), {'slug':self.slug})
    
    @permalink
    def course_expense_groups_url(self):
        return ('course-expense-groups', (), {'slug':self.slug})
    
    @permalink
    def course_lessons_url(self):
        return ('course-lessons', (), {'slug':self.slug})

def course_member_price(course_member, start, end, all_members=None):    
    prices = ExpenseGroupPrice.objects.filter(
              Q(end__gte=start) | Q(end__isnull=True),
            start__lte=end, expense_group__coursemember=course_member,)
    if not prices:
        raise Exception('No price for %s at %s - %s.' % (course_member, start, end))
    
    if all_members is None:
        all_members = course_member.expense_group.coursemember_set.filter(
                    Q(end__gte=start) | Q(end__isnull=True), start__lte=end,)
    else:
        all_members = filter(lambda a:a.expense_group == course_member.expense_group, all_members)
    all_members_count = Decimal(len(all_members))
    
    if not all_members_count:
        raise Exception('Bad date range data for course members for course %s.' % course_member.course)
    
    delta = end - start
    delta_hours = Decimal(delta.days * 24) + Decimal(str(delta.seconds / 3600.0))
    return delta_hours * prices[0].price / all_members_count

class CourseMember(models.Model):
    from schools.students.models import Student
    course = models.ForeignKey('Course')
    student = models.ForeignKey(Student)
    
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    
    expense_group = models.ForeignKey('ExpenseGroup')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return unicode(self.student)
    
    @permalink
    def get_absolute_url(self):
        return ('course-member-detail', (),
            {'slug':self.course.slug,
             'member_id':str(self.pk)})
    
    def create_individual_expense_group(self, price):
        expense_group = ExpenseGroup(course=self.course, name=unicode(self.student))
        expense_group.save()
        expense_group.expensegroupprice_set.create(price=price, start=self.start)
        self.expense_group = expense_group
        return expense_group
            
class Lesson(models.Model):
    from schools.buildings.models import Classroom
    course = models.ForeignKey('Course')
    classroom = models.ForeignKey(Classroom)
    
    start = models.DateTimeField()
    end = models.DateTimeField()
    invoiced = models.BooleanField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        start_format = '%d.%m.%Y %H:%M'
        end_format = '%H:%M' if self.end.date() == self.start.date() else start_format
        
        return '%s: %s - %s' % (self.classroom,
                                format(self.start, start_format),
                                format(self.end, end_format))
        
    def create_attendance_list(self):
        try:
            return self.attendancelist
        except AttendanceList.DoesNotExist:
            return AttendanceList(lesson=self,
                              classroom=self.classroom,
                              lector=self.course.lector,
                              start=self.start, end=self.end)
    
    @permalink
    def get_absolute_url(self):
        return ('course-lesson-detail', (),
                {'slug':self.course.slug, 'lesson_id':str(self.pk)})
        
    @permalink
    def get_attendance_list_url(self):
        return ('course-attendance-list', (),
                {'slug':self.course.slug, 'lesson_id':str(self.pk)})
    
def course_members_on_lesson(course, start, end):
    '''
        Return queryset of all course members who should be 
        on lesson belonging to the course on specified time.
    '''
    return CourseMember.objects.filter(Q(end__isnull=True) | Q(end__gte=start), course=course, start__lte=end)
    
class AttendanceList(models.Model):
    from schools.lectors.models import Lector
    from schools.buildings.models import Classroom
    classroom = models.ForeignKey(Classroom)
    lesson = models.OneToOneField('Lesson')
    lector = models.ForeignKey(Lector)
    
    lector_price = models.DecimalField(max_digits=10, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    content = models.TextField(null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @permalink
    def get_absolute_url(self):
        return ('course-attendance-list', (),
                {'slug':self.lesson.course.slug, 'lesson_id':str(self.lesson.pk)})
        
    def new_course_members(self):
        course_members = CourseMember.objects.exclude(lessonattendee=self)
        return [LessonAttendee(attendance_list=self, course_member=a, present=False) for a in course_members]
    
    def __unicode__(self):
        start_format = 'd.m.Y H:i'
        end_format = 'H:i' if self.start.date() == self.end.date() else start_format
        date_string = '%s - %s' % (dateformat.format(self.start, start_format),
                                   dateformat.format(self.end, end_format))
        return u'%s (%s)' % (self.classroom, date_string)
           
class LessonAttendeeManager(models.Manager):
    def for_invoice(self, company, start, end):
        queryset = self.get_query_set()
        queryset = queryset.filter(course_member__student__company=company,
                                   attendance_list__end__range=(start, end))
        return queryset.filter(invoice__isnull=True)
    
class LessonAttendee(models.Model):
    from schools.invoices.models import Invoice
    objects = LessonAttendeeManager()
    attendance_list = models.ForeignKey('AttendanceList')
    course_member = models.ForeignKey('CourseMember')
    
    present = models.BooleanField(default=True) 
    course_member_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    invoice = models.ForeignKey(Invoice, null=True, blank=True)
    def __unicode__(self):
        return u'%s - %s' % (self.course_member, self.attendance_list)
    
class ExpenseGroup(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey('Course')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @permalink
    def get_absolute_url(self):
        return ('course-expense-group-detail', (),
                {'slug':self.course.slug, 'expense_group_id':str(self.pk)})
        
    def __unicode__(self):
        return self.name
    
class ExpenseGroupPrice(models.Model):
    expense_group = models.ForeignKey('ExpenseGroup')
    
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
