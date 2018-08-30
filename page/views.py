from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import requests

# Create your views here.

urls = {
    'sessions': 'https://glej.parlameter.si/s/seznam-sej/?customUrl=https%3A%2F%2Fanalize.parlameter.si%2Fv1%2Fs%2FgetSessionsList&state=%7B%22filters%22%3A%22Seje%20DZ%22%7D',
    'legislations': 'https://glej.parlameter.si/c/zakonodaja/?state=%7B%22type%22%3A%22Zakoni%22%7D&altHeader=true&customUrl=https%3A%2F%2Fanalize.parlameter.si%2Fv1%2Fs%2FgetAllLegislation%2F',
    'people': 'https://glej.parlameter.si/p/seznam-poslancev/?customUrl=https%3A%2F%2Fanalize.parlameter.si%2Fv1%2Fp%2FgetListOfMembersTickers',
    'organizations': 'https://glej.parlameter.si/ps/seznam-poslanskih-skupin/?customUrl=https%3A%2F%2Fanalize.parlameter.si%2Fv1%2Fpg%2FgetListOfPGs',
}
@login_required(login_url='login')
def view(request):
    page = request.GET.get('page', None)
    if page in urls.keys():
        url = urls[page]
    else:
        url = urls['sessions']

    data = requests.get(url).content
    context = {'embed': data}
    return render(request, 'base_page.html', context)