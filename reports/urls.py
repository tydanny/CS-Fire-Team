from django.urls import path

from . import views

urlpatterns = [
    path('submit/<str:refreshToken>/', views.submit, name='admin_submit'),
	path('officer_submit/<str:refreshToken>/', views.officer_submit, name='officer_submit'),
	path('officer/<str:refreshToken>/', views.officer, name='officer_reports'),
	path('admin/<str:refreshToken>/', views.admin, name='admin_reports'),
]
