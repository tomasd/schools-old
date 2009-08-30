from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class StudentsNav(Nav):
    name = _(u'Students')
    view = 'students'
    nav_group = 'main'
#    options = [TestOption]
    
nav_groups.register(StudentsNav)