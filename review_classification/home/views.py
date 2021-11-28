import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import M
from .forms import ApplicationForm
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
    pred = M.predict(entries)
    res = [[entries[i], pred[i].tolist()] for i in range(len(entries))]

    return HttpResponse(json.dumps(res, indent=4), content_type="application/json")
