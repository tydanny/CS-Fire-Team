from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect

# Create your views here.
def index(request):
    connection = dbconnect()
    connection.connect()
    firstQuery = "SELECT fname FROM PERSON;"
    firsts = connection.run_query(firstQuery)
    lastQuery = "SELECT lname FROM PERSON;"
    lasts = connection.run_query(lastQuery)
    numsQuery = "SELECT id FROM PERSON;"
    nums = connection.run_query(numsQuery)
    empfirst = firsts[1][0]
    emplast = lasts[1][0]
    empNum = nums[1][0]
    testemp = "%s, %s %s" % (emplast, empfirst, empNum)
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
        newPer = "INSERT INTO person (id,fname,lname,title,resident) VALUES ('%s', '%s', '%s', '%s', '%s');" % (empNum, firstName, lastName, title, residency)
        newStat = "INSERT INTO person_status (status, date_change, person_id,) VALUES (%s, %s, %s);" % ("Active", startDate, empNum)
        run_query(newPer)
        run_query(newStat)
        #return HttpResponse(firstName + " " + lastName + " " + str(empNum) + " " + startDate + " " + title + " " + residency)
        return HttpResponse(newPer)
    except:
        return HttpResponse("Error adding data to the database")

def update(request):
    try:
        #Set up for post-changes to update fields: They need to send employee numbers
        employee = request.POST["employee"]
        status = request.POST["status"]
        date = request.POST["date"]
        #statusUpdate = ("INSERT INTO person_status (status, date, empNum) VALUES (%s, %s, %s)" % (status, date, empNum))
        #run_query(statusUpdate)
        return HttpResponse(employee + " " + status + " " + date)
    except:
        return HttpResponse("Error adding data to the database")
