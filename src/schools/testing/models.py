from django.db import models
from django.db.models import permalink

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    max_points = models.IntegerField(default=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @permalink
    def get_absolute_url(self):
        return ('test-detail', (), {'object_id':str(self.pk)})
    
    def __unicode__(self):
        return self.name    

class TestResult(models.Model):
    from schools.courses.models import CourseMember
    test = models.ForeignKey('Test')
    course_member = models.ForeignKey(CourseMember)
    
    points = models.IntegerField()
    date = models.DateField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class CourseMemberAssessment(models.Model):
    from schools.courses.models import CourseMember
    course_member = models.ForeignKey(CourseMember)
    
    description = models.TextField()
    date = models.DateField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)