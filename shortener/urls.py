from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from shortener.views import short_redirect

app_name = 'shortener'
urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('<slug:slug>/', short_redirect, name='url_redirect'),
]
