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
	response = er.get_token_ref(request.POST["username"], request.POST["password"])
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"invalid"}
		return HttpResponse(template.render(context, request))

	db = dbconnect.dbconnect()
	
	user = er.get_my_user(response['access_token'])
	title = db.get_title(user['agencyPersonnelID'])
	refreshToken = response['refresh_token']
	
	if title == 'Fire Chief' or title == 'Deputy Chief' or title == 'Training Officer' or title == 'Administrative Coordinator' or title == 'Deputy Fire Marshall' or title == 'Ops Captain':
		page = 'admin_home'
	elif title == 'Lieutenant' or title == 'Assistant Chief' or title == 'Fire Inspector' or title == 'Shift Officer' or title == 'Captain' or title == 'Administrative Assistant':
		page = 'officer_home'
	elif title == 'Data Collection':
		page = 'admin_home'
	else:
		page = 'user_home'

	template = loader.get_template('submit_redirect.html')
	
	context = {
			'page': page,
			'refreshToken':refreshToken}
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
	
def admin(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))

	if 'time-start' in request.POST.keys() and 'time-end' in request.POST.keys():
		startTime = request.POST['time-start']
		endTime = request.POST['time-end']
		station = "Both"
	else:
		curr = datetime.datetime.now(tz=None)
		startTime = "%s-01-01 00:00:00.00" % curr.year
		endTime = str(curr)
		station = "Both"
	connection = dbconnect.dbconnect()
	nums = connection.get_employee_nums_for_rept()
	totalCalls = connection.dashboard_calls(startTime, endTime, station)
	avgResponders = connection.dashboard_responders(startTime, endTime, station)
	
	
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
		report = rep.Report(str(emp), startTime, endTime)
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

	lastUpdate = connection.get_last_update()
	diff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=6) - lastUpdate

	if diff.days >= 1:
		er.update(response['access_token'], start_date=lastUpdate.isoformat(), end_date=datetime.date.today().isoformat())
		connection.log_update()

	template = loader.get_template('admin_home.html')
	context = {
		'numComplete': numComplete,
		'numOnTrack': numOnTrack,
		'numFalling': numFalling,
		'numBehind': numBehind,
		'avgResponders': avgResponders,
		'totalCalls': totalCalls,
		'refreshToken': response['refresh_token'],
		'lastUpdate': connection.get_last_update().isoformat()
	}
	return HttpResponse(template.render(context, request))

def officer(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))

	if 'time-start' in request.POST.keys() and 'time-end' in request.POST.keys():
		startTime = request.POST['time-start']
		endTime = request.POST['time-end']
		station = "Both"
	else:
		curr = datetime.datetime.now(tz=None)
		startTime = "%s-01-01 00:00:00.00" % curr.year
		endTime = str(curr)
		station = "Both"
	connection = dbconnect.dbconnect()
	nums = connection.get_employee_nums_for_rept()
	totalCalls = connection.dashboard_calls(startTime, endTime, station)
	avgResponders = connection.dashboard_responders(startTime, endTime, station)
	
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
		report = rep.Report(str(emp), startTime, endTime)
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
	template = loader.get_template('officer_home.html')
	context = {'numComplete': numComplete,
			   'numOnTrack': numOnTrack,
			   'numFalling': numFalling,
			   'numBehind': numBehind,
			   'avgResponders': avgResponders,
			   'totalCalls': totalCalls,
			   'refreshToken': response['refresh_token'],
			   'lastUpdate': connection.get_last_update().isoformat()}
	return HttpResponse(template.render(context, request))
	
def user(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
	empNum = er.get_my_user(response['access_token'])['agencyPersonnelID']

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
	db = dbconnect.dbconnect()
	context = {
		'empNum': empNum,
		'employee': fullName,
		'date': str(datetime.date.today()),
		'empStatus': report.statOverall,
		'training': str(report.trainings),
		'trainingStatus': report.statTrainings,
		'shifts': str(report.shifts),
		'bonusShifts': str(report.bonusShifts),
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
		'refreshToken': response['refresh_token'],
		'lastUpdate': db.get_last_update().isoformat()
	}
	return HttpResponse(template.render(context, request))
