from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import Group, Setter

# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    context = {}
    context['groups'] = Group.objects.all()
    return render(request, 'dashboard.html', context)