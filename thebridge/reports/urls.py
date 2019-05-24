from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
	path('officer', views.officer, name='officer'),
	path('admin', views.admin, name='admin'),
]
