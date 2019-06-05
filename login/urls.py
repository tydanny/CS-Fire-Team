from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
	path('', views.login, name='login_page'),
	path('submit', views.check, name='check'),
	path('download/<int:empNum>/', views.user_download, name='download'),
	path('admin_home/<str:refreshToken>/', views.admin, name='admin_home'),
	path('officer_home/<str:refreshToken>/', views.officer, name='officer_home'),
	path('user_home/<str:refreshToken>/', views.user, name='user_ex'),
	path('redirect_user', views.redirect_user, name='redirect_user'),
]