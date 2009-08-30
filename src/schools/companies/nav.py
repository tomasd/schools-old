from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class CompaniesNav(Nav):
    name = _(u'Companies')
    view = 'companies'
    nav_group = 'main'
#    options = [TestOption]
    
nav_groups.register(CompaniesNav)