from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import run_query


# Create your views here.
def index(request):    
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def user(request, username):

    query = "SELECT * FROM PERSON;"

    result = run_query(query)

    return HttpResponse(result)
