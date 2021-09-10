import ast
from django.template.defaultfilters import register


@register.filter(name="isinstance")
def isinstance_filter(val, instance_type):
    return isinstance(val, ast.literal_eval(instance_type))
