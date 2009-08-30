from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class LectorsNav(Nav):
    name = _(u'Lectors')
    view = 'lectors'
    nav_group = 'main'
#    options = [TestOption]
    
nav_groups.register(LectorsNav)