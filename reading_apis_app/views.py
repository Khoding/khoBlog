import requests
from django.shortcuts import render
from jsonview.decorators import json_view


@json_view
def return_the_api(request):
    """Return the API"""
    if "e" not in request.GET:
        return {"error": "Parameter missing"}
    api = request.GET["e"]
    response = requests.get(api)
    thing = response.json()
    if "format" in request.GET:
        f = request.GET["format"]
        if f == "json":
            context = {"things": thing}
            return context
        if f == "api" or f is None or f == "":
            template = "reading_apis_app/list.html"
            context = {"things": thing, "title": "API Reading App"}
            return render(request, template, context)
    else:
        template = "reading_apis_app/list.html"
        context = {"things": thing, "title": "API Reading App"}
        return render(request, template, context)


@json_view
def return_the_api_detail(request):
    """Return the API"""
    if "e" not in request.GET:
        return {"error": "Parameter missing"}
    api = request.GET["e"]
    response = requests.get(api)
    thing = response.json()
    if "format" in request.GET:
        f = request.GET["format"]
        if f == "json":
            context = {"things": thing}
            return context
        if f == "api" or f is None or f == "":
            template = "reading_apis_app/detail.html"
            context = {"things": thing, "title": "API Reading App"}
            return render(request, template, context)
    else:
        template = "reading_apis_app/detail.html"
        context = {"things": thing, "title": "API Reading App"}
        return render(request, template, context)
