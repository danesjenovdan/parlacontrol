from rest_framework import mixins
from rest_framework import generics
from datetime import datetime

from dashboard.models import Group, Setter, Status
from dashboard.serializers import StatusSerializer
from parlacontrol.settings import DATA_URL, ISCI_URL, ANALIZE_URL 

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import requests
import json


def runGroup(request, pk):
    group = get_object_or_404(Group, pk=pk)
    # run script
    return JsonResponse({'status_id': group.status.id})


@csrf_exempt
def runSetter(request, pk, group='setter'):
    if request.method == 'POST':
        print(request.body)
        attr = json.loads(request.body.decode('utf8'))
        if 'attr' in attr.keys():
            attr = attr['attr']
        else:
            attr = ''
        if group == 'setter':
            setter = get_object_or_404(Setter, pk=pk)

            data = {'status_id': setter.status.id,
                    'setters': [setter.setter_name],
                    'type': setter.group.group_type,
                    'is_group': group == 'group',
                    'location': setter.group.location,
                    'attr': attr}
            location = setter.group.location
        else:
            setter = get_object_or_404(Group, pk=pk)

            data = {'status_id': setter.status.id,
                    'setters': [s.setter_name for s in setter.setters.all()],
                    'type': setter.group_type,
                    'is_group': group == 'group',
                    'location': setter.location}
            location = setter.location
        print(location)
        if location == 'parladata':
            print('PARLADATA', data)
            data = json.dumps(data).encode('utf8')
            req = requests.post(DATA_URL + '/tasks/export/',
                                data=data,
                                headers={'content-type': 'application/json'})
        elif location in  ['parlalize', 'p', 'pg']:
            print('PARLALIZE', data)
            data = json.dumps(data).encode('utf8')
            req = requests.post(ANALIZE_URL + '/tasks/',
                                data=data,
                                headers={'content-type': 'application/json'})

        elif location == 'parlasearch':
            print('PARLASEARCH', data)
            data = json.dumps(data).encode('utf8')
            req = requests.post(ISCI_URL + '/tasks/',
                                data=data,
                                headers={'content-type': 'application/json'})
        return JsonResponse({'status_id': setter.status.id})
    else:
        return JsonResponse({'status': 'request isnt post'})


class StatusDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
