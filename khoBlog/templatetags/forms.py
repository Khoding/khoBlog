from django import template

register = template.Library()


@register.inclusion_tag("extras/form_extra.html")
def form(form_obj):
    """Form tag"""
    return {"form": form_obj}


@register.inclusion_tag("extras/form_extra_get.html")
def form_get(form_obj):
    """Form tag"""
    return {"form": form_obj}


@register.inclusion_tag("extras/form_field_extra.html")
def form_field(field):
    """Form field tag"""
    return {
        "field": field,
    }


@register.inclusion_tag("extras/field_label_extra.html")
def field_label(field):
    """Field label tag"""
    return {
        "field": field,
    }
