from django.urls import path

from . import views

urlpatterns = [
	path('user', views.user, name='user_about'),
	path('officer', views.officer, name='officer_about'),
	path('admin', views.admin, name='admin_about'),
]
