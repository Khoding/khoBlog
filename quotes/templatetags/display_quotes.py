from django import template
from django.utils.html import escape, mark_safe

from django_markup.markup import formatter

from quotes.models import Category, Quote

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

    for i, quote in enumerate(quotes):
        if i > 0:
            content.append("<hr>")

        content.append('<blockquote class="quotes">')
        content.append("<dl>")
        body = formatter(quote.body, filter_name="markdown")
        content.append(f"<dt>{body}</dt>")
        content.append("<dd>")
        if quote.author:
            content.append(f"{escape(quote.author.name)}")
        if quote.person:
            for person in quote.person.all():
                content.append(" and ")
                content.append(f"{escape(person.name)}")
        if quote.addressing:
            for i, person in enumerate(quote.addressing.all()):
                if i > 0:
                    content.append(" and ")
                content.append(f" {escape(quote.get_to_or_about_display())} ")
                content.append(f"{escape(person.name)}")
        if quote.source:
            for i, source in enumerate(quote.source.all()):
                if i > 0:
                    content.append(f" and {escape(source.linking_text)} ")
                else:
                    content.append(f" {escape(source.linking_text)} ")

                if source.url:
                    content.append(f'<a href="{source.url}" target="_blank" rel="noopener noreferrer">')
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
        content.append(f'<dd><a href="{quote.get_absolute_url()}">Details for this quote</a></dd>')
        content.append("</dl>")
        content.append("</blockquote>")

    content = "".join(content)
    return mark_safe(content)


@register.simple_tag()
def display_single_quote(o):
    """Display a single quote"""
    quote = Quote.objects.get(slug=o)
    print(quote)

    content = ["<blockquote>", "<dl>"]
    body = formatter(quote.body, filter_name="markdown")
    content.append(f"<dt>{body}</dt>")
    content.append("<dd>")
    if quote.author:
        content.append(f"{escape(quote.author.name)}")
    if quote.person:
        for person in quote.person.all():
            content.append(" and ")
            content.append(f"{escape(person.name)}")
    if quote.addressing:
        for i, person in enumerate(quote.addressing.all()):
            if i > 0:
                content.append(" and ")
            content.append(f" {escape(quote.get_to_or_about_display())} ")
            content.append(f"{escape(person.name)}")
    if quote.source:
        for i, source in enumerate(quote.source.all()):
            if i > 0:
                content.append(f" and {escape(source.linking_text)} ")
            else:
                content.append(f" {escape(source.linking_text)} ")

            if source.url:
                content.append(f'<a href="{source.url}" target="_blank" rel="noopener noreferrer">')
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
