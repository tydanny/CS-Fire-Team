from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about.html/', views.about, name='about'),
    path('<str:username>/', views.user, name='user'),
]
