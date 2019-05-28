from django.urls import path

from . import views


urlpatterns = [
    path('', views.signup, name='create'),
	path('created', views.success, name='success'),
]