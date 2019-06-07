from django.urls import path

from . import views

urlpatterns = [
    path('<str:refreshToken>', views.custom, name='admin_custom'),
	path('officer_custom/<str:refreshToken>', views.officer, name='officer_custom'),
	path('user_custom/<str:refreshToken>', views.user, name='user_custom'),
    path('submit/<str:refreshToken>', views.submit, name='custom_submit'),
	path('officer_submit/<str:refreshToken>', views.officer_submit, name='custom_off_submit'),
	path('user_submit/<str:refreshToken>', views.user_submit, name='custom_user_submit'),
	path('admin_error/<str:refreshToken>', views.error, name='admin_error'),
	path('officer_error/<str:refreshToken>', views.officer_error, name='officer_error'),
	path('user_error/<str:refreshToken>', views.user_error, name='user_error')
]
