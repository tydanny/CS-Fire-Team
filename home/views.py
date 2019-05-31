import sys
sys.path.append('source/')
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import dbconnect
from report import Report
from losap import LOSAP
import datetime
import csv

# Create your views here.
def index(request):    
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
	
def officer(request):
	template = loader.get_template('officer_home.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def admin(request):
	template = loader.get_template('admin_home.html')
	context = {}
	return HttpResponse(template.render(context, request))

def user_download(request, empNum):
    curr = datetime.datetime.now(tz=None)
    startTime = "%s-01-01 00:00:00.00" % curr.year
    endTime = str(curr)
    report = Report(str(empNum), startTime, endTime)
    report.compute_full_report()
    currTime = str(datetime.date.today())
    employee = str(empNum)
    csv_name = "%s_Report_%s.csv" % (employee, currTime)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % csv_name
    writer = csv.writer(response)
    writer.writerow(report.headerRow)
    writer.writerow(report.csvRow)
    return response

def user(request, empNum):
    tarTrainings = 60
    tarShifts = 36
    tarActCalls = 54
    tarWorkDeets = 36
    tarApparatus = 12
    tarFunds = 1
    tarMeets = 6
    curr = datetime.datetime.now(tz=None)
    startTime = "%s-01-01 00:00:00.00" % curr.year
    endTime = str(curr)
    report = Report(str(empNum), startTime, endTime)
    report.compute_full_report()
    losap = LOSAP(str(empNum), startTime, endTime)
    losap.compute_losap()
    fullName = "%s, %s" % (report.lastName, report.firstName)
    
    template = loader.get_template('home_user.html')
    context = {
        'employee': fullName,
        'date': str(datetime.date.today()),
        'empStatus': report.statOverall,
        'training': str(report.trainings),
        'trainingStatus': report.statTrainings,
        'shifts': str(report.shifts),
        'shiftStatus': report.statShifts,
        'actCalls': str(report.actCalls),
        'callStatus': report.statActCalls,
        'workDeets': str(report.WDHours),
        'workDeetStatus': report.statWorkDeets,
        'apparatus': str(report.apparatus),
        'apparatusStatus': report.statApparatus,
        'fundraisers': str(report.fundraisers),
        'fundraiserStatus': report.statFunds,
        'meetings': str(report.meetings),
        'meetingStatus': report.statMeets,
        'leave': losap.total_leave,
        'yrsService': report.yrsService,
    }
    return HttpResponse(template.render(context, request))
