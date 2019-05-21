from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("HOME!")

def user(request, username):
    return HttpResponse("USER Stuff Here Somehow")
