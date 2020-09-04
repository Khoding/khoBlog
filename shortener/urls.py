from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from shortener.views import root

from graphene_django.views import GraphQLView

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('<str:short_url>/', root, name='root'),
]
