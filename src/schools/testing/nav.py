from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class TestsNav(Nav):
    name = _(u'Tests')
    view = 'tests'
    nav_group = 'main'
#    options = [TestOption]
    
nav_groups.register(TestsNav)