from django.urls import path

from . import views

urlpatterns = [
    path('<str:refreshToken>', views.custom, name='admin_custom'),
	path('officer_custom/', views.officer, name='officer_custom'),
	path('user_custom/', views.user, name='user_custom'),
    path('submit/', views.submit, name='custom_submit'),
	path('admin_error/<str:refreshToken>', views.error, name='admin_error'),
]
