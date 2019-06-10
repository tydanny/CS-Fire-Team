from django.urls import path

from . import views

urlpatterns = [
    path('<str:refreshToken>/', views.index, name='import'),
    path('upload/<str:refreshToken>/', views.upload, name='upload'),
	path('refresh/<str:refreshToken>/', views.refresh, name='refresh'),
]
