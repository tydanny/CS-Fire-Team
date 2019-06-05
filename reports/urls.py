from django.urls import path

from . import views

urlpatterns = [
    path('submit/<str:refreshToken>/', views.submit, name='admin_submit'),
	path('officer_submit/', views.officer_submit, name='officer_submit'),
	path('officer/<str:refreshToken>/', views.officer, name='officer_reports'),
	path('admin/<str:refreshToken>/', views.admin, name='admin_reports'),
    path('admin_submit/', views.admin_submit, name='admin_submit'),
]
