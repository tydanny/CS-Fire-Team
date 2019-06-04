from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sys
sys.path.append('..')
from source import er
from source import dbconnect
from source import report as rep
from source import losap as lo
import datetime
import csv

# Create your views here.
def login(request):
	template = loader.get_template('login.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def check(request):
	response = er.get_token_pass(request.POST["username"], request.POST["password"])
	
	print(response)
	
	if response == None:
		template = loader.get_template('login.html')
		context = {"error":"invalid"}
		return HttpResponse(template.render(context, request))
		
	db = dbconnect.dbconnect()
	
	user = er.get_my_user(response)
	title = db.get_title(user['agencyPersonnelID'])
	empNum = user['agencyPersonnelID']
	
	if title == "Firefighter":
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
		report = rep.Report(str(empNum), startTime, endTime)
		report.compute_full_report()
		losap = lo.LOSAP(str(empNum), startTime, endTime)
		losap.compute_losap()
		fullName = "%s, %s" % (report.lastName, report.firstName)
		
		template = loader.get_template('home_user.html')
		context = {
			'empNum': empNum,
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
	elif title == "Officer":
		template = loader.get_template('officer_home.html')
		context = {}
		return HttpResponse(template.render(context, request))
	elif title == "Admin":
		if request.method == "POST":
			startTime = request.POST["time-start"]
			endTime = request.POST["time-end"]
		else:
			curr = datetime.datetime.now(tz=None)
			startTime = "%s-01-01 00:00:00.00" % curr.year
			endTime = str(curr)
		connection = dbconnect()
		numsQuery = "SELECT id FROM PERSON;"
		nums = connection.s_query(numsQuery)
		connection.close()
		
		i = len(nums)
		x = 0
		empNums = []
		reports = []
		numComplete = 0
		numOnTrack = 0
		numFalling = 0
		numBehind = 0
		while x < i:
			emp = nums[x][0]
			empNums.append(emp)
			x += 1
		for emp in empNums:
			report = Report(str(emp), startTime, endTime)
			report.compute_full_report()
			reports.append(report)
		for report in reports:
			if report.statOverall == "Complete":
				numComplete += 1
			elif report.statOverall == "On-Track":
				numOnTrack += 1
			elif report.statOverall == "Falling-Behind":
				numFalling += 1
			elif report.statOverall == "Behind-Schedule":
				numBehind += 1
		template = loader.get_template('admin_home.html')
		context = {'numComplete': numComplete,
				   'numOnTrack': numOnTrack,
				   'numFalling': numFalling,
				   'numBehind': numBehind}
		return HttpResponse(template.render(context, request))
	else:
		template = loader.get_template('login.html')
		context = {"error":"invalid"}
		return HttpResponse(template.render(context, request))
		
def user_download(request, empNum):
    curr = datetime.datetime.now(tz=None)
    startTime = "%s-01-01 00:00:00.00" % curr.year
    endTime = str(curr)
    report = rep.Report(str(empNum), startTime, endTime)
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
	
def admin:
	if request.method == "POST":
		startTime = request.POST["time-start"]
		endTime = request.POST["time-end"]
	else:
		curr = datetime.datetime.now(tz=None)
		startTime = "%s-01-01 00:00:00.00" % curr.year
		endTime = str(curr)
	connection = dbconnect()
	numsQuery = "SELECT id FROM PERSON;"
	nums = connection.s_query(numsQuery)
	connection.close()
	
	i = len(nums)
	x = 0
	empNums = []
	reports = []
	numComplete = 0
	numOnTrack = 0
	numFalling = 0
	numBehind = 0
	while x < i:
		emp = nums[x][0]
		empNums.append(emp)
		x += 1
	for emp in empNums:
		report = Report(str(emp), startTime, endTime)
		report.compute_full_report()
		reports.append(report)
	for report in reports:
		if report.statOverall == "Complete":
			numComplete += 1
		elif report.statOverall == "On-Track":
			numOnTrack += 1
		elif report.statOverall == "Falling-Behind":
			numFalling += 1
		elif report.statOverall == "Behind-Schedule":
			numBehind += 1
	template = loader.get_template('admin_home.html')
	context = {'numComplete': numComplete,
			   'numOnTrack': numOnTrack,
			   'numFalling': numFalling,
			   'numBehind': numBehind}
	return HttpResponse(template.render(context, request))

def officer:
	template = loader.get_template('officer_home.html')
	context = {}
	return HttpResponse(template.render(context, request))
	
def user:
	tarTrainings = 60
	tarShifts = 36
	tarActCalls = 54
	tarWorkDeets = 36
	tarApparatus = 12
	tarFunds = 1
	tarMeets = 6
	##
	empNum = 1
	##
	curr = datetime.datetime.now(tz=None)
	startTime = "%s-01-01 00:00:00.00" % curr.year
	endTime = str(curr)
	report = rep.Report(str(empNum), startTime, endTime)
	report.compute_full_report()
	losap = lo.LOSAP(str(empNum), startTime, endTime)
	losap.compute_losap()
	fullName = "%s, %s" % (report.lastName, report.firstName)

	template = loader.get_template('home_user.html')
	context = {
		'empNum': empNum,
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


	