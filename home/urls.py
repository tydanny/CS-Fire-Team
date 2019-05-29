from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
	path('1', views.user, name='user_ex'),
    path('<int:empNum>/', views.user, name='user_home'),
    path('<int:empNum>/download/', views.user_download, name='user_home_download'),
	path('officer', views.officer, name='officer_home'),
	path('admin', views.admin, name='admin_home'),
]
