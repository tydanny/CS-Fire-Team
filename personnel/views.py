from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from source import dbconnect, er

# Create your views here.
def index(request, refreshToken):
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
    template = loader.get_template('admin_personnel.html')
    context = {
		'employees' : emps, 
		'refreshToken': response['refresh_token']
	}
    return HttpResponse(template.render(context, request))

def update(request, refreshToken):
    response = er.refresh(refreshToken)
	
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))

    try:
        connection = dbconnect.dbconnect()
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        status = request.POST["status"]
        date = request.POST["date"]
        note = request.POST["text"]
        connection.load_person_status(status, date, str(empNum), note)
        connection.close()
        template = loader.get_template('submit.html')
        context = {
			'refreshToken': response['refresh_token']
		}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('admin_error.html')
        context = {}
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
		
	
