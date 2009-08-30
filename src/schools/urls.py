from django.conf.urls.defaults import * #@UnusedWildImport

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
import django_nav

admin.autodiscover()
django_nav.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^skoly/', include('skoly.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/(.*)', admin.site.root),
     url(r'^building', include('buildings.urls')),
     url(r'^course', include('courses.urls')),
     url(r'^lector', include('lectors.urls')),
     url(r'^student', include('students.urls')),
     url(r'^company', include('companies.urls')),
     url(r'^test', include('testing.urls')),
     url(r'^$', direct_to_template, {'template':'base.html'}),
     url(r'^invoice', include('invoices.urls')),
#     url(r'^management/', include('management.urls')),
)
