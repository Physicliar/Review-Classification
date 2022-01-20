import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import ApplicationForm
from .models import Application
import requests


def index(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data.get("appId")
            return HttpResponseRedirect('/reviews/%s/' % data)
        form = ApplicationForm()
    form = ApplicationForm()
    context = {
        'form': form
    }
    return render(request, 'home/contact.html', context)


def review(request, app_id):
    url = "https://itunes.apple.com/rss/customerreviews/id=" + app_id + "/sortBy=mostRecent/json"
    request = requests.get(url)
    data = request.json()
    entries = [entry['content']['label'] for entry in data['feed']['entry']]
    s = []
    for i, e in enumerate(entries):
        s.append({
            "id": i,
            "content": e,
            "informative": True,
            "bugReport": False,
            "featureRequest": False,
            "praise": True,
            "critic": False,
        })
    return HttpResponse(json.dumps(s, indent=4), content_type="application/json")
