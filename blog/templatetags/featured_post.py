from blog.models import Post
from django import template

register = template.Library()


@register.inclusion_tag("tailwind/featured_posts.html")
def featured_post_list(urls):
    """featured_post_list Every Featured Posts for links lists"""
    urls = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"urls": urls}


@register.inclusion_tag("tailwind/super_featured_objects.html")
def super_featured_post_list(objects):
    """super_featured_post_list Every Super Featured Posts for links lists"""
    objects = Post.objects.defer("body", "image").filter(featuring_state="SF")
    return {"objects": objects}
