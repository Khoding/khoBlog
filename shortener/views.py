from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from graphene_django.views import GraphQLView
from khoBlog.utils.superuser_required import superuser_required

from .models import URL


def short_redirect(request, slug):
    url = get_object_or_404(URL, slug=slug)
    url.clicked()

    return redirect(url.full_url)


@superuser_required()
class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass
