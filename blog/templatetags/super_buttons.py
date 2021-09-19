from django import template

register = template.Library()


@register.inclusion_tag('blog/includes/super_buttons.html')
def sb(o):
    return {'object': o}
