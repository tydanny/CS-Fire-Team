from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.template import loader
from dbconnect import dbconnect

from forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('success')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
	
	
def success(request):
	template = loader.get_template('success.html')
	context = {}
	return HttpResponse(template.render(context, request))