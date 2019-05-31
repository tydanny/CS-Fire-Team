from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect

# Create your views here.
def custom(request):
	template = loader.get_template('admin_custom.html')
	context = {}
	return HttpResponse(template.render(context, request))