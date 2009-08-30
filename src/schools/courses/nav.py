from django_nav import nav_groups, Nav
from django.utils.translation import ugettext_lazy as _


class CoursesNav(Nav):
    name = _(u'Courses')
    view = 'courses'
    nav_group = 'main'
#    options = [TestOption]
    
nav_groups.register(CoursesNav)