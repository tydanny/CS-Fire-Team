from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import datetime
from source import dbconnect, er

"""
Generate the appropriate about page for the
corresponding view (i.e. the user about page
does not have any information about generating
reports for others)
"""

# Create your views here.
def user(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))

	template = loader.get_template('user_about.html')
	context = {'refreshToken': response['refresh_token']}
	return HttpResponse(template.render(context, request))
	
def officer(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
	
	template = loader.get_template('officer_about.html')
	context = {
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))
	
def admin(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))

	if request.method == "POST":
		startTime = request.POST["time-start"]
		endTime = request.POST["time-end"]
	else:
		curr = datetime.datetime.now(tz=None)
		startTime = "%s-01-01 00:00:00.00" % curr.year
		endTime = str(curr)
	connection = dbconnect.dbconnect()
	numsQuery = "SELECT id FROM PERSON;"
	nums = connection.s_query(numsQuery)
	connection.close()
	template = loader.get_template('admin_about.html')
	context = {
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))
