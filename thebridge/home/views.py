from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect


# Create your views here.
def index(request):    
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def user(request, username):
    connection = dbconnect()
    connection.connect()
    query = "SELECT * FROM PERSON;"

    result = connection.run_query(query)

    return HttpResponse(result)
