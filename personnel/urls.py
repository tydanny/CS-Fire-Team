from django.urls import path

from . import views

urlpatterns = [
    path('<str:refreshToken>/', views.index, name='personnel'),
    path('update/', views.update, name='update'),
]
