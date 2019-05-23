from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect

# Create your views here.
def index(request):
    connection = dbconnect()
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
    template = loader.get_template('reports.html')
    context = {'employees' : emps}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        startDate = request.POST["time-start"]
        endDate = request.POST["time-end"]
        reportType = request.POST["type"]
        staff = request.POST.getlist("staff")
        connection = dbconnect()
        if staff[0] == "Generate For All":
            connection.generate_for_all(startDate, endDate, reportType)
        elif len(staff) == 1:
            nums = [int(s) for s in staff[0].split() if s.isdigit()]
            empNum = nums[-1]
            connection.generate_for_individual(empNum, startDate, endDate, reportType)
        else:
            empNums = []
            for person in staff:
                nums = [int(s) for s in staff[0].split() if s.isdigit()]
                empNums.append(nums[-1])
                connection.generate_for_some(empNums, startDate, endDate, reportType)
        connection.close()
        template = loader.get_template('submit.html')
        context = {}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))
