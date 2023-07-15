import requests
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from jsonview.decorators import json_view


def check_admin(user):
    """check_admin checks if the user is an admin"""
    return user.is_superuser


@user_passes_test(check_admin)
@json_view
def return_the_api(request):
    """Return the API"""
    f = "api"
    if "e" in request.GET:
        api = request.GET["e"]
        response = requests.get(api)
        thing = response.json()
    else:
        f = "json"
        thing = {"error": "No API provided"}
    if "format" in request.GET:
        f = request.GET["format"]
    if f == "json":
        context = {"things": thing}
        return context
    template = "reading_apis_app/list.html"
    context = {"things": thing, "title": "API Reading App"}
    return render(request, template, context)


@user_passes_test(check_admin)
@json_view
def return_the_api_detail(request):
    """Return the API"""
    f = "api"
    if "e" in request.GET:
        api = request.GET["e"]
        response = requests.get(api)
        thing = response.json()
    else:
        f = "json"
        thing = {"error": "No API provided"}
    if "format" in request.GET:
        f = request.GET["format"]
    if f == "json":
        context = {"things": thing}
        return context
    template = "reading_apis_app/detail.html"
    context = {"things": thing, "title": "API Reading App"}
    return render(request, template, context)
