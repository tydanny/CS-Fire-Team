from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
import csv

class DataInput(forms.Form):
    file = forms.FileField()

# Create your views here.
def index(request):
    template = loader.get_template('admin_import.html')
    context = {}
    return HttpResponse(template.render(context, request))

def upload(request):
    if request.method == "POST":
        csv_file = DataInput(request.POST, request.FILES)
        csv_lines = csv.reader(csv_file.cleaned_data["file"])
        for line in csv_lines:
            print(line)
        return HttpResponse("SUCCESS")
    else:
        return HttpResponse("OH NOOOO")
