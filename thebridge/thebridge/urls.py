"""thebridge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('home/', include('home.urls')),
    path('about/', include('about.urls')),
    path('reports/', include('reports.urls')),
    path('personnel/', include('personnel.urls')),
    path('import/', include('import.urls')),
    path('logout/', include('logout.urls')),
    path('admin/', admin.site.urls),
	path('accounts/', include('accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('loggedout/', TemplateView.as_view(template_name='logged_out.html'), name = "loggedout"),
    path('homepage/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', TemplateView.as_view(template_name='redirect.html'), name='redirect'),
]
