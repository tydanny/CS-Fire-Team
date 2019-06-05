from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from source import converters


# Create your views here.
def index(request, refreshToken):
    template = loader.get_template('admin_import.html')
    context = {}
    return HttpResponse(template.render(context, request))

def upload(request):
    try:
        myfile = request.FILES['fileToUpload']
        template = loader.get_template('submit.html')
        context = {}
        
        #I dont know if this works or if changes need to be made to account for django stuff
        converters.convert_iar(myfile)
        
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('error.html')
        context = {}
        return HttpResponse(template.render(context, request))