from django.contrib.contenttypes.models import ContentType
from django.template import Library, Node, TemplateSyntaxError, Variable

register = Library()


def _get_content_types(tagname, tokens):
    """Gets content types from tag tokens"""
    content_types = []
    for token in tokens:
        try:
            app, model = token.split(".")
            content_types = ContentType.objects.get(app_label=app, model=model)
        except ValueError:
            raise TemplateSyntaxError("Argument %s in %r must be in the format 'app.model'" % (token, tagname))
        except ContentType.DoesNotExist:
            raise TemplateSyntaxError("ContentType '%s.%s' used for tag %r doesn't exist" % (app, model, tagname))
    return content_types


class BaseLastElementsNode(Node):
    """Base class to deal with the last N XtdComments for a list of app.model"""

    def __init__(self, count, content_types, template_path=None):
        """Class method to parse get_xtdcomment_list and return a Node."""
        try:
            self.count = int(count)
        except Exception:
            self.count = Variable(count)

        self.content_types = content_types
        self.template_path = template_path


class GetLastElementsNode(BaseLastElementsNode):
    """Gets the last element of the node"""

    def __init__(self, count, as_varname, content_types):
        super(GetLastElementsNode, self).__init__(count, content_types)
        self.as_varname = as_varname

    def render(self, context):
        """Render"""
        if not isinstance(self.count, int):
            self.count = int(self.count.resolve(context))
        q_object = self.content_types.model_class()
        self.qs = q_object.objects.all()[: self.count]
        context[self.as_varname] = self.qs
        return ""


@register.tag
def get_objects(parser, token):
    """
    Get the last N of an Object.

    Syntax::

        {% get_objects N as var for app.model [app.model] %}

    Example usage::

        {% get_objects 5 as objects for blog.story blog.quote %}

    """
    tokens = token.contents.split()

    try:
        count = int(tokens[1])
    except ValueError:
        raise TemplateSyntaxError("Second argument in %r tag must be a integer" % tokens[0])

    if tokens[2] != "as":
        raise TemplateSyntaxError("Third argument in %r tag must be 'as'" % tokens[0])

    as_varname = tokens[3]

    if tokens[4] != "for":
        raise TemplateSyntaxError("Fifth argument in %r tag must be 'for'" % tokens[0])

    content_types = _get_content_types(tokens[0], tokens[5:])
    return GetLastElementsNode(count, as_varname, content_types)
