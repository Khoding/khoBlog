import requests
from django.shortcuts import render
from jsonview.decorators import json_view


@json_view
def return_the_api(request):
    """Return the API"""
    if "e" not in request.GET:
        return None
    api = request.GET["e"]
    response = requests.get(api)
    thing = response.json()
    f = "api"
    if "format" in request.GET:
        f = request.GET["format"]
    if f == "json":
        context = {"things": thing}
        return context
    if f == "api":
        template = "reading_apis_app/list.html"
        context = {"things": thing, "title": "API Reading App"}
        return render(request, template, context)


@json_view
def return_the_api_detail(request):
    """Return the API"""
    if "e" not in request.GET:
        return None
    api = request.GET["e"]
    response = requests.get(api)
    thing = response.json()
    f = "api"
    if "format" in request.GET:
        f = request.GET["format"]
    if f == "json":
        context = {"things": thing}
        return context
    if f == "api":
        template = "reading_apis_app/detail.html"
        context = {"things": thing, "title": "API Reading App"}
        return render(request, template, context)
