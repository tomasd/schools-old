from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class BuildingsNav(Nav):
    name = _(u'Buildings')
    view = 'buildings'
    nav_group = 'main'
#    options = [TestOption]
    
nav_groups.register(BuildingsNav)