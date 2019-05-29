from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='reports'),
    path('submit/', views.submit, name='submit_report'),
	path('officer', views.officer, name='officer_reports'),
	path('admin', views.admin, name='admin_reports'),
]
