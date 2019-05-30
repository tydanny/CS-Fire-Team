from django.urls import path

from . import views

urlpatterns = [
    path('submit/', views.submit, name='admin_submit'),
	path('officer_submit/', views.officer_submit, name='officer_submit'),
	path('officer', views.officer, name='officer_reports'),
	path('admin', views.admin, name='admin_reports'),
]
