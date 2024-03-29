from django import template

register = template.Library()


@register.tag(name="evaluate")
def do_evaluate(parser, token):
    """tag usage {% evaluate object.textfield %}"""
    try:
        _unused_tag_name, variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(f"{token.contents.split()[0]} tag requires a single argument")
    return EvaluateNode(variable)


class EvaluateNode(template.Node):
    """Evaluates a node"""

    def __init__(self, variable):
        """Initialize"""
        self.variable = template.Variable(variable)

    def render(self, context):
        """Render"""
        try:
            content = self.variable.resolve(context)
            t = template.Template(content)
            return t.render(context)
        except (template.VariableDoesNotExist, template.TemplateSyntaxError):
            return "Error rendering", self.variable
