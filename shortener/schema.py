import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from .models import URL


class URLType(DjangoObjectType):
    class Meta:
        model = URL


class Query(graphene.ObjectType):
    urls = graphene.List(
        URLType, url=graphene.String(), first=graphene.Int(), skip=graphene.Int()
    )

    @staticmethod
    def resolve_urls(info, url=None, first=None, skip=None, **kwargs):
        queryset = URL.objects.all()

        if url:
            _filter = Q(full_url__icontains=url)
            queryset = queryset.filter(_filter)

        if first:
            queryset = queryset[:first]

        if skip:
            queryset = queryset[skip:]

        return queryset


class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    class Arguments:
        full_url = graphene.String()
        title = graphene.String()

    @staticmethod
    def mutate(info, full_url, title):
        url = URL(full_url=full_url, title=title)
        url.save()

        return CreateURL(url=url)


class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()
