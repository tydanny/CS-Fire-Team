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
    report.compute_shifts()
    report.compute_act_calls()
    report.compute_total_calls()
    report.compute_work_detail_hours()
    report.compute_apparatus()
    report.compute_fundraisers()
    report.compute_meetings()
    report.compute_trainings()
    return HttpResponse(str(report.trainings) + " " + str(report.totTrainings))
