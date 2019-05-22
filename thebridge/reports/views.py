from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect

# Create your views here.
def index(request):
    connection = dbconnect()
    connection.connect()
    firstQuery = "SELECT fname FROM PERSON;"
    firsts = connection.s_query(firstQuery)
    lastQuery = "SELECT lname FROM PERSON;"
    lasts = connection.s_query(lastQuery)
    numsQuery = "SELECT id FROM PERSON;"
    nums = connection.s_query(numsQuery)
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
    template = loader.get_template('reports.html')
    context = {'employees' : emps}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        test = ""
        i = 0
        thingies = []
        for thingy in request.POST:
            thingies.append(thingy)
        startDate = request.POST["time-start"]
        endDate = request.POST["time-end"]
        reportType = request.POST["type"]
        staff = request.POST.getlist("staff")
        template = loader.get_template('submit.html')
        context = {}
        #return HttpResponse(template.render(context, request))
        return HttpResponse(staff)
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))
