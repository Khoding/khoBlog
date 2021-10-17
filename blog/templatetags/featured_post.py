from blog.models import Post
from django import template

register = template.Library()


@register.inclusion_tag("blog/lists/links_list.html", takes_context=True)
def featured_big_post_list(context, urls):
    urls = Post.objects.defer("body", "image").filter(featuring_state="FB")
    return {"urls": urls, "context": context}


@register.inclusion_tag("blog/lists/links_list.html", takes_context=True)
def featured_post_list(context, urls):
    urls = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"urls": urls, "context": context}


@register.inclusion_tag("blog/includes/featured_posts.html")
def featured_big_posts():
    featured_big = Post.objects.defer("body", "image").filter(featuring_state="FB")
    o = featured_big.order_by("?")[0]
    return {"featured_big": o}


@register.inclusion_tag("blog/includes/featured_posts.html")
def featured_posts():
    featured = Post.objects.defer("body", "image").filter(featuring_state="F")
    return {"featured": featured}
