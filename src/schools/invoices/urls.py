from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
   url(r'invoice/$', 'courses', name='courses'),
   url(r'(?P<invoice_slug>[-\w]+)/$', 'invoice_detail', name='invoice-detail'),
)
