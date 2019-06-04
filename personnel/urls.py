from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='personnel'),
    path('update/', views.update, name='update'),
]
