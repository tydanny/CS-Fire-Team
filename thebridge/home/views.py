from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect
from report import Report
import datetime

# Create your views here.
def index(request):    
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def user(request, empNum):
    curr = datetime.datetime.now(tz=None)
    startTime = "%s-01-01 00:00:00.00" % curr.year
    endTime = str(curr)
    report = Report(str(empNum), startTime, endTime)
    report.compute_full_report()
    fullName = "%s, %s" % (report.lastName, report.firstName)
    template = loader.get_template('home_user.html')
    context = {
        'employee': fullName,
        'date': endTime,
        'training': str(report.trainings),
        'shifts': str(report.shifts),
        'actCalls': str(report.actCalls),
        'workDeets': str(report.WDHours),
        'apparatus': str(report.apparatus),
        'fundraisers': str(report.fundraisers),
        'meetings': str(report.meetings),
    }
    return HttpResponse(template.render(context, request))
