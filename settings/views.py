from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    userInfo = request.user

    context = {'userInfo': userInfo}
    return render(request, 'settings/userProfile.html', context)
