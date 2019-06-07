from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from source import converters, er


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
        template = loader.get_template('submit.html')
        
        #I dont know if this works or if changes need to be made to account for django stuff
        converters.convert_iar(myfile)
        context = {
            'refreshToken': response['refresh_token']
        }
        
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        template = loader.get_template('error.html')
        context = {
            'refreshToken': response['refresh_token']
        }
        return HttpResponse(template.render(context, request))