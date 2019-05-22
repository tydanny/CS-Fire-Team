from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('update/', views.update, name='update'),
    path('note/', views.note, name='note'),
]
