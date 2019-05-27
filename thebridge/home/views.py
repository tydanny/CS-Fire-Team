import sys
sys.path.append('/home/ty/Desktop/CS-Fire-Team/thebridge/source/')
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import dbconnect
import report
import datetime

# Create your views here.
def index(request):    
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
	
def userhome(request):
	template = loader.get_template('user_home.html')
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
    fullName = "%s, %s" % (report.lastName, report.firstName)

    daysPassed = (datetime.date.today() - datetime.date(curr.year, 1, 1)).days
    tarRatio = daysPassed / 365
    ratTrains = report.trainings / tarTrainings
    ratShifts = report.shifts / tarShifts
    ratActCalls = report.actCalls / tarActCalls
    ratWorkDeets = report.WDHours / tarWorkDeets
    ratApparatus = report.apparatus / tarApparatus
    ratFunds = report.fundraisers / tarFunds
    ratMeets = report.meetings / tarMeets

    statTrainings = "On-Track"
    statShifts = "On-Track"
    statActCalls = "On-Track"
    statWorkDeets = "On-Track"
    statApparatus = "On-Track"
    statFunds = "On-Track"
    statMeets = "On-Track"

    if tarRatio - 0.2 >= ratTrains:
        statTrainings = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratTrains:
        statTrainings = "Falling-Behind"
    elif ratTrains >= 0.99:
        statTrainings = "Complete"

    if tarRatio - 0.2 >= ratShifts:
        statShifts = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratShifts:
        statShifts = "Falling-Behind"
    elif ratShifts >= 0.99:
        statShifts = "Complete"

    if tarRatio - 0.2 >= ratActCalls:
        statActCalls = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratActCalls:
        statActCalls = "Falling-Behind"
    elif ratActCalls >= 0.99:
        statActCalls = "Complete"

    if tarRatio - 0.2 >= ratWorkDeets:
        statWorkDeets = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratWorkDeets:
        statWorkDeets = "Falling-Behind"
    elif ratWorkDeets >= 0.99:
        statWorkDeets = "Complete"

    if tarRatio - 0.2 >= ratApparatus:
        statApparatus = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratApparatus:
        statApparatus = "Falling-Behind"
    elif ratApparatus >= 0.99:
        statApparatus = "Complete"

    if tarRatio - 0.2 >= ratFunds:
        statFunds = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratFunds:
        statFunds = "Falling-Behind"
    elif ratFunds >= 0.99:
        statFunds = "Complete"

    if tarRatio - 0.2 >= ratMeets:
        statMeets = "Behind-Schedule"
    elif tarRatio - 0.1 >= ratMeets:
        statMeets = "Falling-Behind"
    elif ratMeets >= 0.99:
        statMeets = "Complete"

    generalStat = "On-Track"
    if (statTrainings == "Complete" and statShifts == "Complete" and statActCalls == "Complete"):
        if (statWorkDeets == "Complete" and statApparatus == "Complete" and statFunds == "Complete" and statMeets == "Complete"):
            generalStat = "Complete"
    elif (statTrainings == "Behind-Schedule" or statShifts == "Behind-Schedule" or statActCalls == "Behind-Schedule"):
        generalStat = "Behind-Schedule"
    elif (statWorkDeets == "Behind-Schedule" or statApparatus == "Behind-Schedule" or statFunds == "Behind-Schedule" or statMeets == "Behind-Schedule"):
        generalStat = "Behind-Schedule"
    elif (statTrainings == "Falling-Behind" or statShifts == "Falling-Behind" or statActCalls == "Falling-Behind"):
        generalStat = "Falling-Behind"
    elif (statWorkDeets == "Falling-Behind" or statApparatus == "Falling-Behind" or statFunds == "Falling-Behind" or statMeets == "Falling-Behind"):
        generalStat = "Falling-Behind"
    
    template = loader.get_template('home_user.html')
    context = {
        'employee': fullName,
        'date': str(datetime.date.today()),
        'empStatus': generalStat,
        'training': str(report.trainings),
        'trainingStatus': statTrainings,
        'shifts': str(report.shifts),
        'shiftStatus': statShifts,
        'actCalls': str(report.actCalls),
        'callStatus': statActCalls,
        'workDeets': str(report.WDHours),
        'workDeetStatus': statWorkDeets,
        'apparatus': str(report.apparatus),
        'apparatusStatus': statApparatus,
        'fundraisers': str(report.fundraisers),
        'fundraiserStatus': statFunds,
        'meetings': str(report.meetings),
        'meetingStatus': statMeets,
    }
    return HttpResponse(template.render(context, request))
