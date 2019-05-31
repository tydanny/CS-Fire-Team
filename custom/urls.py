from django.urls import path

from . import views

urlpatterns = [
    path('', views.custom, name='admin_custom'),
]
