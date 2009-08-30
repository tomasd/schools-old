from django.conf.urls.defaults import * #@UnusedWildImport
from django.views.generic.create_update import update_object
from schools import object_list
from schools.invoices.forms import InvoiceForm
from schools.invoices.models import Invoice

urlpatterns = patterns('invoices.views',
#   url(r'invoice/$', 'courses', name='courses'),
#   url(r'(?P<invoice_slug>[-\w]+)/$', 'invoice_detail', name='invoice-detail'),
    url(r'^create/$', 'create_invoice', name='invoice-create'),
    url(r'(?P<object_id>\d+)/attendees/$', 'invoice_lesson_attendees', name='invoice-lesson-attendees'),
    url(r'(?P<object_id>\d+)/$', update_object, dict(
                form_class=InvoiceForm,
                login_required=True,
                template_object_name='invoice',), name='invoice-detail'),
    url(r'/$', object_list, {'queryset':Invoice.objects.all(),
                           'login_required':True,
                           'template_object_name':'invoice'}, name='invoices'),
)
