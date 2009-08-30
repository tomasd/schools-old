from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import create_object, update_object
from schools import object_list
from schools.students.forms import StudentForm
from schools.students.models import Student

urlpatterns = patterns('',
   url(r'^create/$', create_object, dict(
                form_class=StudentForm,
                login_required=True,
                template_name='students/student_create.html'), name='student-create'),
   url(r'(?P<object_id>\d+)/$', update_object, dict(
                form_class=StudentForm,
                login_required=True,
                template_object_name='student',), name='student-detail'),
   url(r'/$', object_list, {'template_object_name':'student',
                           'login_required':True, 
                           'queryset':Student.objects.all()}, name='students'),
)