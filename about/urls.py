from django.urls import path

from . import views

urlpatterns = [
	path('user/<str:refreshToken>/', views.user, name='user_about'),
	path('officer/<str:refreshToken>/', views.officer, name='officer_about'),
	path('admin/<str:refreshToken>/', views.admin, name='admin_about'),
]
