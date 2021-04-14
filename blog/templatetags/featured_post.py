from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/links_list.html')
def featured_big_post_list(urls):
    urls = Post.objects.filter(
        featuring_state='FB')
    return {'urls': urls}


@register.inclusion_tag('blog/links_list.html')
def featured_post_list(urls):
    urls = Post.objects.filter(
        featuring_state='F')
    return {'urls': urls}
