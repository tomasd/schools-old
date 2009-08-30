from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import create_object, update_object
from schools import object_list
from schools.lectors.forms import LectorForm
from schools.lectors.models import Lector

urlpatterns = patterns('lectors.views',
   url(r'create/$', create_object, {'form_class':LectorForm,
                                    'login_required':True,
                                    'template_name':'lectors/lector_create.html'}, name='lector-create'),
   url(r'(?P<lector_id>\d+)/contract/$', 'contracts', name='lector-contracts'),
   url(r'(?P<lector_id>\d+)/contract/(?P<contract_id>\d+)/$', 'contract_detail', name='lector-contract-detail'),
   url(r'(?P<object_id>\d+)/$', update_object, 
       {'form_class':LectorForm, 'login_required':True, 'template_object_name':'lector'}, name='lector-detail'),
   url(r'/$', object_list, {'login_required':True,
                            'queryset':Lector.objects.all(),
                            'template_object_name':'lector',
                            }, name='lectors'),
)
