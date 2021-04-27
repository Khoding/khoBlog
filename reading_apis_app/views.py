from django.shortcuts import render
import requests


def home(request):
    if 'endpoint' in request.GET:
        api = request.GET['endpoint']
        url = api
        response = requests.get(url)
        thing = response.json()
        return render(request, 'reading_apis_app/detail.html', {
            'things': thing,
            'title': 'API Reading App'
        })
