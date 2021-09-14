from django import template

from ..models import Post

register = template.Library()


@register.inclusion_tag('blog/object_snippet.html')
def render_latest_blog_entries(num, summary_first=False, hide_readmore=False, hide_header=False,
                               header_tag=''):
    if not str(num) == "*":
        entries = Post.objects.get_base_common_queryset()[:num]
    else:
        entries = Post.objects.get_base_common_queryset()
    return {
        'entries': entries,
        'summary_first': summary_first,
        'header_tag': header_tag,
        'hide_header': hide_header,
        'hide_readmore': hide_readmore,
    }
