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
    i = len(firsts)
    x = 0
    emps = []
    while x < i:
        empfirst = firsts[x][0]
        emplast = lasts[x][0]
        empNum = nums[x][0]
        emp = "%s, %s %s" % (emplast, empfirst, empNum)
        emps.append(emp)
        x += 1
    template = loader.get_template('personnel.html')
    context = {'employees' : emps}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        connection = dbconnect()
        connection.connect()
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]
        empNum = request.POST["empNumber"]
        startDate = request.POST["time-start"]
        title = request.POST["title"]
        residency = request.POST["residency"]
        newPer = "INSERT INTO person (id,fname,lname,title,resident) VALUES ('%s','%s','%s','%s','%s');" % (empNum, firstName, lastName, title, residency)
        newStat = "INSERT INTO person_status (status, date_change, person_id,) VALUES (%s, %s, %s);" % ("Active", startDate, empNum)
        connection.run_query(newPer)
        connection.run_query(newStat)
        #return HttpResponse(firstName + " " + lastName + " " + str(empNum) + " " + startDate + " " + title + " " + residency)
        template = loader.get_template('submit.html')
        context = {}
        #return HttpResponse(newPer)
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))

def update(request):
    try:
        connection = dbconnect()
        connection.connect()
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        status = request.POST["status"]
        date = request.POST["date"]
        statusUpdate = ("INSERT INTO person_status (status, date, empNum) VALUES (%s, %s, %s)" % (status, date, empNum))
        connection.run_query(statusUpdate)
        #return HttpResponse(str(empNum) + " " + status + " " + date)
        template = loader.get_template('submit.html')
        context = {}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))
