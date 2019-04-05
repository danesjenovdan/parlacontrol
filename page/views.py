from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.views import LoginView

import requests
import logging

logger = logging.getLogger('django')

logger.info('TEST')
logger.info('+'*100)

# Create your views here.

urls = {
    'sessions': settings.GLEJ_URL + '/dashboard/sessions',
    'legislation': settings.GLEJ_URL + '/dashboard/legislation',
    'people': settings.GLEJ_URL + '/dashboard/people',
    'organizations': settings.GLEJ_URL + '/dashboard/organisations',
    'votings': settings.GLEJ_URL + '/dashboard/votings',
    'tagger': settings.GLEJ_URL + '/dashboard/tagger',
}

@login_required(login_url='login')
def view(request):
    page = request.GET.get('page', None)
    session = request.GET.get('session', None)

    logger.info(session)

    if page in urls.keys():
        url = urls[page]
        if page == 'votings' and session is not None:
            url += '?state={"session":' + str(session) + '}'
    else:
        url = urls['sessions']

    logger.info(url)

    data = requests.get(url).content
    context = {'embed': data}
    return render(request, 'page/base.html', context)
