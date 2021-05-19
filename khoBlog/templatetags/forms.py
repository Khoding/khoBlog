from django import template

register = template.Library()


@register.inclusion_tag('extras/form_extra.html')
def form(form_obj):
    return {'form': form_obj}


@register.inclusion_tag('extras/form_field_extra.html')
def form_field(field):
    return {
        'field': field,
    }


@register.inclusion_tag('extras/field_label_extra.html')
def field_label(field):
    return {
        'field': field,
    }
