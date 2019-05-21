from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import run_query

# Create your views here.
def index(request):

    empQuery = 'SELECT last, first FROM PERSON SORT BY last DESC;'

    employees = run_query(empQuery)

    template = loader.get_template('personnel.html')
    context = {'employees' : employees}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]
        empNum = request.POST["empNumber"]
        startDate = request.POST["time-start"]
        title = request.POST["title"]
        residency = request.POST["residency"]
        newPer = "INSERT INTO person (id,fName,lName,title,residency) VALUES (%s, %s, %s, %s, %s)" % (empNum, firstName, lastName, title, residency)
        newStat = "INSERT INTO person_status (status, date_change, person_id,) VALUES (%s, %s, %s)" % ("Active", startDate, empNum)
        run_query(newPer)
        run_query(newStat)
        return HttpResponse(firstName + " " + lastName + " " + str(empNum) + " " + startDate + " " + title + " " + residency)
    except:
        return HttpResponse("Error adding data to the database")

def update(request):
    try:
        employee = request.POST["employee"]
        status = request.POST["status"]
        return HttpResponse(employee + " " + status)
    except:
        return HttpResponse("Error adding data to the database")
