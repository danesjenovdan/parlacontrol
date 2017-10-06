from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import Group, Setter

from parlacontrol.settings import DATA_URL, API_AUTH, ANALIZE_URL, PARLALIZE_API_KEY, PAGE_URL

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

    context.update(getLastSessionUrls())
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def motions_view(request, page, untagged, search=None):
    print("Search", search)
    context = {}
    context['motions'], pagination = getMotions(int(untagged), page, search)
    context['tags'] = getAllTags()

    context['pagination'] = pagination
    context['untagged'] = int(untagged)
    context['data_url'] = DATA_URL

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
    remove_tags = ['fb', 'social', 'tag1', 'Ljubljana', 'center', 'facebook', 'tw']
    while True:
        data = getAuthParladataRequest('/tags/?page=' + str(idx))
        out += [{'name': tag['name'], 'id': tag['id']}
                for tag
                in data['results']
                if tag['name'] not in remove_tags]
        if not data['next']:
            break
        idx += 1
    return out


def getLastSessionUrls():
    data = getAuthParladataRequest('/last_session')
    session_id = data['results'][0]['id']
    set_motions = ANALIZE_URL + '/s/setMotionOfSession/' + str(session_id) + '/?key=' + PARLALIZE_API_KEY
    fr_motions = PAGE_URL + '/seja/glasovanja/' + str(session_id) + '?forceRender=true'
    fr_last_session = ANALIZE_URL + '/utils/recacheLastSession/?key=' + PARLALIZE_API_KEY
    
    groups = {'last_session': [{'name': 'setters',
                                'setters': [{'name': 'set motion of session',
                                             'url': set_motions,
                                             'type': 'silent'}]},
                               {'name': 'recache',
                                'setters': [{'name': 'recache motions',
                                             'url': fr_motions,
                                             'type': 'new_tab'},
                                            {'name': 'recache last session',
                                             'url': fr_last_session,
                                             'type': 'silent'}]}
                               ]
              }
    return groups