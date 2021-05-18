from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/links_list.html', takes_context=True)
def featured_big_post_list(context, urls):
    urls = Post.objects.filter(
        featuring_state='FB')
    return {'urls': urls, 'context': context}


@register.inclusion_tag('blog/links_list.html', takes_context=True)
def featured_post_list(context, urls):
    urls = Post.objects.filter(
        featuring_state='F')
    return {'urls': urls, 'context': context}
