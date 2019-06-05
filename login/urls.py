from django.urls import path

from . import views

urlpatterns = [
	path('', views.login, name='login_page'),
	path('submit', views.check, name='check'),
	path('download/<int:empNum>/', views.user_download, name='download'),
	path('admin_home', views.admin, name='admin_home'),
	path('officer_home', views.officer, name='officer_home'),
	path('user_home', views.user, name='user_ex'),
	path('redirect_user', views.redirect_user, name='redirect_user'),
]