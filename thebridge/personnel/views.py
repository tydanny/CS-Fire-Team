from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import run_query

# Create your views here.
def index(request):

    empQuery = "SELECT fname FROM PERSON;"

    employees = run_query(empQuery)
    testemp = employees[0][0]

    template = loader.get_template('personnel.html')
    context = {'testemp' : testemp}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]
        empNum = request.POST["empNumber"]
        startDate = request.POST["time-start"]
        title = request.POST["title"]
        residency = request.POST["residency"]
        newPer = ("INSERT INTO person (id,fName,lName,title,residency) VALUES (%s, %s, %s, %s, %s)" % (empNum, firstName, lastName, title, residency))
        newStat = ("INSERT INTO person_status (status, date_change, person_id) VALUES (%s, %s, %s)" % ("Active", startDate, empNum))
        run_query(newPer)
        run_query(newStat)
        return HttpResponse(firstName + " " + lastName + " " + str(empNum) + " " + startDate + " " + title + " " + residency)
    except:
        return HttpResponse("Error adding data to the database")

def update(request):
    try:
        #Set up for post-changes to update fields: They need to send employee numbers
        empNum = request.POST["empNum"]
        status = request.POST["status"]
        date = request.POST["date"]
        statusUpdate = ("INSERT INTO person_status (status, date, empNum) VALUES (%s, %s, %s)" % (status, date, empNum))
        return HttpResponse(employee + " " + status + " " + date)
    except:
        return HttpResponse("Error adding data to the database")
