from django.urls import path

from . import views

urlpatterns = [
    path('<str:refreshToken>/', views.index, name='personnel'),
    path('update/<str:refreshToken>/', views.update, name='update'),
	path('error/<str:refreshToken>/', views.error, name='personnel_error'),
	path('get/<str:refreshToken>/', views.get, name='get'),
]
