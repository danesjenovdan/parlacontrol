from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import Group, Setter

from parlacontrol.settings import DATA_URL, API_AUTH

import requests
from requests.auth import HTTPBasicAuth

# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    context = {}
    context['groups'] = Group.objects.all()
    context['motions'], pagination = getMotions()
    context['tags'] = getAllTags()
    context['username'] = API_AUTH[0]
    context['password'] = API_AUTH[1]
    context['data_url'] = DATA_URL

    context['pagination'] = pagination
    context['untagged'] = 0

    print("ivan", context)
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def motions_view(request, page, untagged, search=None):
    print("Search", search)
    context = {}
    context['motions'], pagination = getMotions(int(untagged), page, search)
    context['tags'] = getAllTags()

    context['pagination'] = pagination
    context['untagged'] = int(untagged)

    #default paginator

    return render(request, 'motions.html', context)


def getMotions(untagged=0, page=1, search=None):
    if search:
        search = "&search="+search
    else:
        search = ""
    if untagged:
        motions = getAuthParladataRequest('/unedited_motions/?page=' + str(page) + search)
    else:
        motions = getAuthParladataRequest('/motions/?page=' + str(page) + search)

    pagination = {'prev': int(page) - 1 if (motions['previous']) else None, 
                  'current': int(page), 
                  'next': int(page) + 1 if (motions['next']) else None, }

    for motion in motions['results']:
        vote = getAuthParladataRequest('/votes/' + str(motion['vote'][0]))
        motion['start_time'] = vote['start_time']
        motion['tags'] = vote['tags']
        motion['vote'] = motion['vote'][0]
        motion['results'] = vote['results']
    return motions, pagination


def getAuthParladataRequest(endpoint):
    data = requests.get(DATA_URL + endpoint,
                        auth=HTTPBasicAuth(API_AUTH[0], API_AUTH[1])).json()

    return data


def getAllTags():
    idx = 1
    out = []
    while True:
        data = getAuthParladataRequest('/tags/?page=' + str(idx))
        out += [{'name': tag['name'], 'id': tag['id']} for tag in data['results']]
        if not data['next']:
            break
        idx += 1
    return out
