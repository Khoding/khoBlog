from django import template
from django.utils.html import escape, mark_safe

from django_markup.markup import formatter

from quotes.models import Quote, Category

register = template.Library()

# display the quotes in a simple tag
@register.simple_tag()
def display_quotes(category_slug, show_category_title=False):
    """Display quotes"""
    category = Category.objects.get(slug=category_slug)
    quotes = Quote.objects.filter(category=category)

    content = [""]

    if show_category_title:
        content.append(f'<h2 id="{category.slug}">{category.title}</h2>')

    for i, item in enumerate(quotes):
        if i > 0:
            content.append("<hr>")

        content.append("<blockquote>")
        content.append("<dl>")
        body = formatter(item.body, filter_name="markdown")
        body = formatter(body, filter_name="widont")
        content.append(f"<dt>{body}</dt>")
        content.append("<dd>")
        if item.author:
            content.append(f"{escape(item.author.name)}")
        if item.person:
            for person in item.person.all():
                content.append(" and ")
                content.append(f"{escape(person.name)}")
        if item.addressing:
            for i, person in enumerate(item.addressing.all()):
                if i > 0:
                    content.append(" and ")
                content.append(f" {escape(item.get_to_or_about_display())} ")
                content.append(f"{escape(person.name)}")
        if item.source:
            for i, source in enumerate(item.source.all()):
                if i > 0:
                    content.append(" and in ")
                else:
                    content.append(" in ")
                if source.url:
                    content.append(f"<a href='{source.url}'>")
                content.append(f"{escape(source.title)}")
                if source.url:
                    content.append("</a>")

                if source.date:
                    content.append(f" ({escape(format(source.date, source.date_type))}")
                    if not source.media:
                        content.append(")")
                if source.media:
                    if source.date:
                        content.append(", ")
                    else:
                        content.append(" (")
                    content.append(f"{escape(source.media.title)}")
                    content.append(")")
        content.append("</dd>")
        content.append("</dl>")
        content.append("</blockquote>")

    content = "".join(content)
    return mark_safe(content)
