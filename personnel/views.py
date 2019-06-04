from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from source import dbconnect

# Create your views here.
def index(request):
    connection = dbconnect.dbconnect()
    firstQuery = "SELECT fname FROM PERSON;"
    firsts = connection.s_query(firstQuery)
    lastQuery = "SELECT lname FROM PERSON;"
    lasts = connection.s_query(lastQuery)
    numsQuery = "SELECT id FROM PERSON;"
    nums = connection.s_query(numsQuery)
    connection.close()
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
    template = loader.get_template('admin_personnel.html')
    context = {'employees' : emps}
    return HttpResponse(template.render(context, request))
	
'''

def submit(request):
    try:
        connection = dbconnect.dbconnect()
        firstName = request.POST["firstname"]
        lastName = request.POST["lastname"]
        empNum = request.POST["empNumber"]
        startDate = request.POST["time-start"]
        title = request.POST["title"]
        residency = request.POST["residency"]
        newPer = "INSERT INTO person (id,fname,lname,title,resident) VALUES ('%s','%s','%s','%s','%s');" % (empNum, firstName, lastName, title, residency)
        newStat = "INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '%s', '%s');" % (startDate, empNum)
        connection.i_query(newPer)
        connection.i_query(newStat)
        connection.close()
        template = loader.get_template('submit.html')
        context = {}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))
		'''

def update(request):
    try:
        connection = dbconnect.dbconnect()
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        status = request.POST["status"]
        date = request.POST["date"]
        note = request.POST["text"]
        connection.load_person_status(status, date, str(empNum), note)
        connection.close()
        template = loader.get_template('submit.html')
        context = {}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))
