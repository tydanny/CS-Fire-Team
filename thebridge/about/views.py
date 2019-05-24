from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('about.html')
    context = {}
    return HttpResponse(template.render(context, request))
	
def user(request):
	template = loader.get_template('user_about.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def officer(request):
	template = loader.get_template('officer_about.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def admin(request):
	template = loader.get_template('admin_about.html')
	context = {}
	return HttpResponse(template.render(context, request))
