from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from source import dbconnect, detail_reports, er
import csv

"""
Generates the custom reports page for officers and
admins
"""

# Create your views here.
def officer(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
	connection = dbconnect.dbconnect()
	people = connection.get_active_people()
	emps = []
	for p in people:
		emp = "%s, %s %s" % (p[2], p[1], p[0])
		emps.append(emp)
		
	curr = datetime.datetime.now(tz=None)
	defaultStart = "%s-01-01" % curr.year
	defaultEnd = str(curr)

	template = loader.get_template('officer_custom.html')
	context = {
		'employees': emps, 
		'defaultStart' : defaultStart,
		'defaultEnd' : defaultEnd,
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))

def user(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))

	curr = datetime.datetime.now(tz=None)
	defaultStart = "%s-01-01" % curr.year
	defaultEnd = str(curr)

	template = loader.get_template('user_custom.html')
	context = {
		'refreshToken': response['refresh_token'],
		'defaultStart' : defaultStart,
		'defaultEnd' : defaultEnd,
		'empNum': er.get_my_user(response['access_token'])['agencyPersonnelID']
	}
	return HttpResponse(template.render(context, request))

def custom(request, refreshToken):
    response = er.refresh(refreshToken)
	
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))

    connection = dbconnect.dbconnect()
    people = connection.get_active_people()
    emps = []
    for p in people:
        emp = "%s, %s %s" % (p[2], p[1], p[0])
        emps.append(emp)
		
    curr = datetime.datetime.now(tz=None)
    defaultStart = "%s-01-01" % curr.year
    defaultEnd = str(curr)
	
    template = loader.get_template('admin_custom.html')
    context = {
		'employees': emps,
        'defaultStart' : defaultStart,
        'defaultEnd' : defaultEnd,
		'refreshToken': response['refresh_token']
	}
    return HttpResponse(template.render(context, request))

def submit(request, refreshToken):
    try:
        startTime = request.POST["time-start"]
        endTime = request.POST["time-end"]
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        reportType = request.POST["type"]
        detailReport = detail_reports.Event_Detail_Report(str(empNum), startTime, endTime, reportType)
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
        template = loader.get_template('admin_error.html')
        context = {'refreshToken': refreshToken}
        return HttpResponse(template.render(context, request))
		
def officer_submit(request, refreshToken):
    try:
        startTime = request.POST["time-start"]
        endTime = request.POST["time-end"]
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        reportType = request.POST["type"]
        detailReport = detail_reports.Event_Detail_Report(str(empNum), startTime, endTime, reportType)
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
        template = loader.get_template('officer_error.html')
        context = {'refreshToken': refreshToken}
        return HttpResponse(template.render(context, request))
		
def user_submit(request, refreshToken, empNum):
    try:
        startTime = request.POST["time-start"]
        endTime = request.POST["time-end"]
        reportType = request.POST["type"]
        detailReport = detail_reports.Event_Detail_Report(str(empNum), startTime, endTime, reportType)
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
        template = loader.get_template('user_error.html')
        context = {'refreshToken': refreshToken}
        return HttpResponse(template.render(context, request))