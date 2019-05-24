from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:empNum>/', views.user, name='user'),
	path('user', views.userhome, name='userhome'),
]
