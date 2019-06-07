from django.urls import path

from . import views

urlpatterns = [
    path('<str:refreshToken>', views.custom, name='admin_custom'),
	path('officer_custom/<str:refreshToken>', views.officer, name='officer_custom'),
	path('user_custom/<str:refreshToken>', views.user, name='user_custom'),
    path('submit/', views.submit, name='custom_submit'),
	path('officer_submit/', views.officer_submit, name='custom_off_submit'),
	path('admin_error/<str:refreshToken>', views.error, name='admin_error'),
	path('officer_error/<str:refreshToken>', views.officer_error, name='officer_error')
]
