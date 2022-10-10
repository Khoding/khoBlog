from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.html import escape, mark_safe

from django_markup.markup import formatter

from quotes.models import Quote

register = template.Library()


@register.simple_tag()
def display_quotes(model_class, model_slug, show_title=False):
    """Display quotes"""
    content_type = ContentType.objects.get(app_label="Quotes", model=model_class)
    lookup_container = content_type.get_object_for_this_type(slug=model_slug)
    filter_object = content_type.name
    filters = {filter_object: lookup_container}
    filter_q = Q(**filters)
    if filter_object == "person":
        filter_q = Q(author=lookup_container) | Q(person=lookup_container) | Q(addressing=lookup_container)
    QUOTES = Quote.objects.filter(filter_q)

    content = [""]

    if show_title:
        content.append(f'<h2 id="{lookup_container.slug}">{lookup_container.title}</div>')

    for i, quote in enumerate(QUOTES):
        if i > 0:
            content.append("<hr>")

        content.append('<blockquote class="quotes quote_list">')
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
            for qai, person in enumerate(quote.addressing.all()):
                if qai > 0:
                    content.append(" and")
                content.append(f" {escape(quote.get_to_or_about_display())} ")
                content.append(f"{escape(person.name)}")
        if quote.source:
            for qsi, source in enumerate(quote.source.all()):
                if qsi > 0:
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

    content = ["<blockquote class='quotes'>", "<dl>"]
    body = formatter(quote.body, filter_name="markdown")
    content.append(f"<dt>{body}</dt>")
    content.append("<dd>")
    if quote.author:
        content.append(f"<a href='{quote.author.get_absolute_url()}'>{escape(quote.author.name)}</a>")
    if quote.person:
        for person in quote.person.all():
            content.append(" and ")
            content.append(f"<a href='{person.get_absolute_url()}'>{escape(person.name)}</a>")
    if quote.addressing:
        for i, person in enumerate(quote.addressing.all()):
            if i > 0:
                content.append(" and ")
            content.append(f" {escape(quote.get_to_or_about_display())} ")
            content.append(f"<a href='{person.get_absolute_url()}'>{escape(person.name)}</a>")
    if quote.source:
        for i, source in enumerate(quote.source.all()):
            if i > 0:
                content.append(f" and {escape(source.linking_text)} ")
            else:
                content.append(f" {escape(source.linking_text)} ")

            content.append(f'<a href="{source.get_absolute_url()}">{escape(source.title)}</a>')

            if source.url:
                content.append(f' <a href="{source.url}" target="_blank" rel="noopener noreferrer">Go to source</a>')

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
