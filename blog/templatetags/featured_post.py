from blog.models import Post
from django import template

register = template.Library()


@register.inclusion_tag("tailwind/featured_posts.html")
def featured_post_list(urls):
    """featured_post_list_n Every Featured Posts for links lists"""
    urls = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"urls": urls}


@register.inclusion_tag("tailwind/featured_big_posts.html")
def featured_big_post_list(objects):
    """featured_big_post_list_n Every Featured Big Posts for links lists"""
    objects = Post.objects.defer("body", "image").filter(featuring_state="FB")
    return {"objects": objects}
