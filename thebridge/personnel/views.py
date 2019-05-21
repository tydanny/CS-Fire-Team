from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import run_query
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
        title = request.POST[""]
        newPer = "INSERT INTO person (id,fName,lName,title) VALUES (%s, %s, %s, %s)", (empNum, firstName, lastName, title)
        newStat = "INSERT INTO person_status (status, date_change, person_id,) VALUES (%s, %s, %s)", ("Active", startDate, empNum)
        run_query(newPer)
        run_query(newStat)
        return HttpResponse(firstName + " " + lastName + " " + str(empNum) + " " + startDate)
    except:
        return HttpResponse("Error adding data to the database")
