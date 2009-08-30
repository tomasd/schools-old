from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import create_object, update_object
from schools import object_list
from schools.testing.forms import TestForm
from schools.testing.models import Test

urlpatterns = patterns('',
   url(r'create/$', create_object,
       { 'form_class': TestForm,
        'login_required':True,
        'template_name':'testing/test_create.html' }, name='test-create'),
        
   url(r'(?P<object_id>\d+)/$', update_object,
       {'form_class':TestForm, 'login_required':True,
        'template_object_name':'test'}, name='test-detail'),
   url(r'/$', object_list,
       {'login_required':True,
        'template_object_name':'test',
        'queryset':Test.objects.all()}, name='tests'),
)
