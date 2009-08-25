import IPython.ipapi #@UnresolvedImport
ip = IPython.ipapi.get()

def load_django_models():
    try:
        from django.db.models.loading import get_models
        for m in get_models():
            try:
                ip.ex("from %s import %s" % (m.__module__, m.__name__))
            except ImportError:
                print "ERROR: Import of %s from %s failed." % (m.__name__, m.__module__)                
                pass
        print 'INFO: Loaded Django models.'
    except ImportError:
        pass

def init_django():
    import settings
    from django.core.management import setup_environ
    setup_environ(settings)

    load_django_models()
    import localeurl.middleware #@UnusedImport
    from django.core.urlresolvers import reverse
    from django.test import Client
    ip.user_ns['client'] = Client()
    ip.user_ns['reverse'] = reverse
    print 'INFO: Created client instance.'

init_django()
