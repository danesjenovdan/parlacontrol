from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from dashboard.models import Group, Setter, Cron, ActiveCron

from parlacontrol.settings import (DATA_URL, API_AUTH, ANALIZE_URL, PARLALIZE_API_KEY,
                                   PAGE_URL, SERVER_USER, SPS_JS)

import requests
import json

from requests.auth import HTTPBasicAuth

from crontab import CronTab

# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    context = {}
    context['groups'] = Group.objects.all()
    context['motions'], pagination = getMotions()
    context['tags'] = getAllTags()
    context['crontabs'] = getAllCrontabs()
    context['sessions'] = getSessionsDatas()
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
    context['username'] = API_AUTH[0]
    context['password'] = API_AUTH[1]

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

    sps = SPS_JS
    
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
                                             'type': 'silent'},
                                            {'name': 'recache sps-js',
                                             'url': sps,
                                             'type': 'new_tab'}]}
                               ]
              }
    return groups


def getAllCrontabs():
    return Cron.objects.all()


@login_required(login_url='login')
@csrf_exempt
def addCron(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf8'))
        attr = data.get('attr', None)
        cron_id = data.get('cron_id', None)
        print(cron_id)
        cron = Cron.objects.get(id=cron_id)
        command = cron.command
        if cron.has_attr:
            if not attr:
                raise Http404('attr missing')
            else:
                command = command.replace('XXXX', str(attr))

        user_crons = CronTab(SERVER_USER)
        is_exist = bool(list(user_crons.find_command(command)))
        if is_exist:
            print("ALERT")
        else:
            new_cron = user_crons.new(command)
            if cron.hour:
                add_cron_time(new_cron.hour, cron.hour)
            if cron.minute:
                add_cron_time(new_cron.minute, cron.minute)
            if cron.day:
                add_cron_time(new_cron.dow, cron.day)

            new_cron.enable()

            ActiveCron(cron=cron,
                       full_command=str(new_cron),
                       command=command).save()

            user_crons.write()

    context = {}
    context['crontabs'] = getAllCrontabs()
    print(context)
    return render(request, 'crons.html', context)


@login_required(login_url='login')
@csrf_exempt
def deleteCron(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf8'))
        cron_id = data.get('cron_id', None)
        aCron = ActiveCron.objects.get(id=cron_id)

        user_crons = CronTab('tomaz')
        cron = user_crons.find_command(aCron.command)
        crons = list(cron)
        if crons:
            user_crons.remove(crons[0])
            aCron.delete()
            user_crons.write()
        else:
            print('ni tega crona')
    else:
        print('ni post')
    context = {}
    context['crontabs'] = getAllCrontabs()
    print(context)
    return render(request, 'crons.html', context)

def add_cron_time(cron_time, time):
    if '-' in time:
        args = time.split('-')
        cron_time.during(*args)
    else:
        cron_time.on(time)



def getSessionsDatas():
    sessions = getAuthParladataRequest('/sessions/?organization=95&ordering=-start_time')
    sessions = sessions['results']
    return sessions