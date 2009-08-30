import re

from django import template

from django_nav import nav_groups

register = template.Library()

class GetNavNode(template.Node):
    def __init__(self, nav_group, var_name):
            self.nav_group = nav_group
            self.var_name = var_name
            self.context = {'request': ''}

    def render(self, context):
        self.context = context
        self.build_nav()
        return ''

    def build_nav(self):
        self.context[self.var_name] = []

        for nav in nav_groups[self.nav_group]:
            nav.option_list = self.build_options(nav.options)
            nav.active = False
            if self.context['request'].path == nav.get_absolute_url():
                nav.active = True

            self.context[self.var_name].append(template.loader.render_to_string(nav.template, {'nav': nav}))

    def build_options(self, tab_options):
        options = []
        for option in tab_options:
            option.option_list = self.build_options(option.options)
            options.append(template.loader.render_to_string(option.template, {'option': option}))

        return options

def get_nav(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    m = re.search(r'(.*?) as (\w+)', args)
    if not m:
        nav_group = var_name = args.strip("'").strip('"')
    else:
        nav_group, var_name = m.groups()
        nav_group = nav_group.strip("'").strip('"')

    return GetNavNode(nav_group, var_name)

register.tag('get_nav', get_nav)
