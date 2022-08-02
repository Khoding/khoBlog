from django import template

from ..models import Post

register = template.Library()


@register.inclusion_tag("tailwind/changelog.html")
def changelog():
    """A changelog of latest changes."""
    objects = Post.objects.filter(postcatslink__category__slug="updates").get_base_common_queryset()[:7]
    return {"objects": objects}
