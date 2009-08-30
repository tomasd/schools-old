from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import create_object, update_object
from schools import object_list
from schools.companies.forms import CompanyForm
from schools.companies.models import Company

urlpatterns = patterns('',
   url(r'^create/$', create_object, dict(
                form_class=CompanyForm,
                login_required=True,
                template_name='companies/company_create.html'), name='company-create'),
   url(r'(?P<object_id>\d+)/$', update_object, dict(
                form_class=CompanyForm,
                login_required=True,
                template_object_name='company',), name='company-detail'),
   url(r'/$', object_list, {'template_object_name':'company',
                           'login_required':True, 
                           'queryset':Company.objects.all()}, name='companies'),
)
