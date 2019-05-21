from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):    
    template = loader.get_template('personnel.html')
    context = {}
    return HttpResponse(template.render(context, request))


def submit(request):
    try:
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]
        empNum = request.POST["empNumber"]
        startDate = request.POST["time-start"]
        return HttpResponse(firstName + " " + lastName + " " + str(empNum) + " " + startDate)
    except:
        return HttpResponse("Error adding data to the database")
