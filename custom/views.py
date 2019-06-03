from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect
from detail_reports import Event_Detail_Report
import csv

# Create your views here.
def officer(request):
	template = loader.get_template('officer_custom.html')
	context = {}
	return HttpResponse(template.render(context, request))

def user(request):
	template = loader.get_template('user_custom.html')
	context = {}
	return HttpResponse(template.render(context, request))

def custom(request):
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
    template = loader.get_template('admin_custom.html')
    context = {'employees': emps}
    return HttpResponse(template.render(context, request))

def submit(request):
    try:
        startTime = request.POST["time-start"]
        endTime = request.POST["time-end"]
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        reportType = request.POST["type"]
        detailReport = Event_Detail_Report(str(empNum), startTime, endTime, reportType)
        csv_name = "%s_Event_Detail_Report_%s_%s.csv" %(str(empNum), startTime, endTime)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % csv_name
        writer = csv.writer(response)
        writer.writerow(detailReport.headerRow)
        for row in detailReport.csvRows:
            writer.writerow(row)
        return response        
    except Exception as e:
        print(e)
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))
