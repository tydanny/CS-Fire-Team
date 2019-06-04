from django.urls import path

from . import views

urlpatterns = [
	path('', views.login, name='login'),
	path('submit', views.check, name='check'),
	path('download/<int:empNum>/', views.user_download, name='download')
]