from blog.models import Post
from django import template

register = template.Library()


@register.inclusion_tag('blog/links_list.html', takes_context=True)
def featured_big_post_list(context, urls):
    urls = Post.objects.defer('body', 'image').filter(
        featuring_state='FB')
    return {'urls': urls, 'context': context}


@register.inclusion_tag('blog/links_list.html', takes_context=True)
def featured_post_list(context, urls):
    urls = Post.objects.defer('body', 'image').filter(
        featuring_state='F')
    return {'urls': urls, 'context': context}
