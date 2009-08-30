from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class InvoicesNav(Nav):
    name = _(u'Invoices')
    view = 'invoices'
    nav_group = 'main'
#    options = [TestOption]
    
#nav_groups.register(InvoicesNav)