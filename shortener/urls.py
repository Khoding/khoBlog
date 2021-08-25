from shortener.views import short_redirect
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import PrivateGraphQLView

app_name = 'shortener'
urlpatterns = [
    path('graphql/', csrf_exempt(PrivateGraphQLView.as_view(graphiql=True))),
    path('<slug:slug>/', short_redirect, name='url_redirect'),
]
