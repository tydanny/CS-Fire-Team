from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from source import converters, er, dbconnect

"""
Creates the import page for admins. This page
calls the update function when the refresh button
is clicked and calls converters.py when an I Am
Responding scheduling report is uploaded.
"""

# Create your views here.
def index(request, refreshToken):
    response = er.refresh(refreshToken)

    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))


    template = loader.get_template('admin_import.html')
    context = {
        'refreshToken': response['refresh_token']
    }
    return HttpResponse(template.render(context, request))

def upload(request, refreshToken):
    response = er.refresh(refreshToken)

    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))

    try:
        myfile = request.FILES['fileToUpload']
        if r"iar_refresh" in request.POST.keys():
            checked = True
        else:
            checked = False
        startTime = request.POST['time-start']
        endTime = request.POST['time-end']
        template = loader.get_template('admin_submit.html')
        converters.convert_iar(myfile, checked, startTime, endTime)
        
        context = {
            'refreshToken': response['refresh_token']
        }
        
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        template = loader.get_template('admin_error.html')
        context = {
            'refreshToken': response['refresh_token']
        }
        return HttpResponse(template.render(context, request))
		
def refresh(request, refreshToken):
    response = er.refresh(refreshToken)
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error": "access_error"}
        return HttpResponse(template.render(context, request))
    try:
        start = request.POST['time-start']
        end = request.POST['time-end']

        db = dbconnect.dbconnect()
        db.delete(start, end)
        er.update(response['access_token'], start_date=start, end_date=end)

        template = loader.get_template('admin_submit.html')
        context = {'refreshToken': response['refresh_token']}
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        template = loader.get_template('admin_error.html')
        context = {'refreshToken': response['refresh_token']}
        return HttpResponse(template.render(context, request))
