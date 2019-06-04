from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='import'),
    path('upload/', views.upload, name='upload'),
]
