from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from shortener.views import short_redirect

from graphene_django.views import GraphQLView

app_name = 'shortener'
urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('<slug:slug>/', short_redirect, name='url_redirect'),
]
