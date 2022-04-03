from blog.models import Post
from django import template

register = template.Library()


@register.inclusion_tag("blog/lists/links_list.html", takes_context=True)
def featured_big_post_list(context, urls):
    """featured_big_post_list Every Featured Big Posts for links lists"""
    urls = Post.objects.defer("body", "image").filter(featuring_state="FB")
    return {"urls": urls, "context": context}


@register.inclusion_tag("blog/lists/links_list.html", takes_context=True)
def featured_post_list(context, urls):
    """featured_post_list Every Featured Posts for links lists"""
    urls = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"urls": urls, "context": context}


@register.inclusion_tag("tailwind/featured_posts_n.html")
def featured_post_list_n(urls):
    """featured_post_list_n Every Featured Posts for links lists"""
    urls = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"urls": urls}


@register.inclusion_tag("tailwind/featured_big_posts_n.html")
def featured_big_post_list_n(objects):
    """featured_big_post_list_n Every Featured Big Posts for links lists"""
    objects = Post.objects.defer("body", "image").filter(featuring_state="FB")
    return {"objects": objects}


@register.inclusion_tag("blog/includes/featured_posts.html")
def featured_big_posts():
    """featured_big_posts Every Featured Big Posts"""
    featured_big = Post.objects.defer("body", "image").filter(featuring_state="FB")
    if not featured_big:
        return None
    o = featured_big.order_by("?")[0]
    return {"featured_big": o}


@register.inclusion_tag("blog/includes/featured_posts.html")
def featured_posts():
    """featured_posts Every Featured Posts"""
    featured = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"featured": featured}
