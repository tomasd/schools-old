from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import create_object, update_object
from schools import object_list
from schools.buildings.forms import BuildingForm
from schools.buildings.models import Building

urlpatterns = patterns('buildings.views',
   url(r'(?P<building_id>\d+)/classroom/(?P<classroom_id>\d+)/$', 'classroom_detail', name='classroom-detail'),
   url(r'(?P<building_id>\d+)/classroom/create/$', 'classroom_create', name='classroom-create'),
   url(r'(?P<building_id>\d+)/classroom/$', 'classrooms', {'template_name':'buildings/building_classrooms.html', 'template_object_name':'classroom'}, name='classrooms'),
         
   url(r'(?P<building_id>\d+)/expense/(?P<building_expense_id>\d+)/$', 'building_expense_detail', name='building-expense-detail'),
   url(r'(?P<building_id>\d+)/expense/create/$', 'building_expense_create', name='building-expense-create'),
   url(r'(?P<building_id>\d+)/expense/$', 'building_expenses', {'template_name':'buildings/building_expenses.html', 'template_object_name':'building_expense'}, name='building-expenses'),

   url(r'^create/$', create_object, dict(
                form_class=BuildingForm,
                login_required=True,
                template_name='buildings/building_create.html'), name='building-create'),
   url(r'(?P<object_id>\d+)/$', update_object, dict(
                form_class=BuildingForm,
                login_required=True,
                template_object_name='building',), name='building-detail'),
   url(r'$', object_list, {'queryset':Building.objects.all(), 
                           'login_required':True,
                           'template_object_name':'building'}, name='buildings'),
)
