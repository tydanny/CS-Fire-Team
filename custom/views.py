from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from source import dbconnect, detail_reports, er
import csv

# Create your views here.
def officer(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
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

	template = loader.get_template('officer_custom.html')
	context = {
		'employees': emps, 
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))

def user(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))

	template = loader.get_template('user_custom.html')
	context = {
		'refreshToken': response['refresh_token'],
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
    context = {
		'employees': emps, 
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
		
def error(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
	template = loader.get_template('admin_error.html')
	context = {
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))
	
def officer_error(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
	template = loader.get_template('officer_error.html')
	context = {
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))
	
def user_error(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
	template = loader.get_template('user_error.html')
	context = {
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))
	