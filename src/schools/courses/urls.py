from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import create_object, update_object
from schools import object_list
from schools.courses.forms import CourseForm
from schools.courses.models import Course

urlpatterns = patterns('courses.views',
   url(r'create/$', create_object, 
       { 'form_class': CourseForm,
        'login_required':True,
        'template_name':'courses/course_create.html' }, name='course-create'),
        
   url(r'(?P<slug>[-\w]+)/member/(?P<member_id>\d+)/$', 'course_member_detail', name='course-member-detail'),
   url(r'(?P<slug>[-\w]+)/member/$', 'course_members', name='course-members'),
   
   url(r'(?P<slug>[-\w]+)/lesson/(?P<lesson_id>\d+)/attendance/$', 'course_attendance_list', name='course-attendance-list'),
   url(r'(?P<slug>[-\w]+)/lesson/(?P<lesson_id>\d+)/$', 'course_lesson_detail', name='course-lesson-detail'),
   url(r'(?P<slug>[-\w]+)/lesson/$', 'course_lessons', name='course-lessons'),
   
   url(r'(?P<slug>[-\w]+)/expense-group/$', 'course_expense_groups_list', name='course-expense-groups'),
   url(r'(?P<slug>[-\w]+)/expense-group/(?P<expense_group_id>\d+)/$', 'course_expense_group_detail', name='course-expense-group-detail'),

   url(r'(?P<slug>[-\w]+)/$', update_object,
       {'form_class':CourseForm, 'login_required':True}, name='course-detail'),
   url(r'$', object_list, 
       {'login_required':True,
        'template_object_name':'course',
        'queryset':Course.objects.all()}, name='courses'),
)
