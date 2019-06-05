from django.urls import path

from . import views

urlpatterns = [
    path('import/<str:refreshToken>/', views.index, name='import'),
    path('upload/<str:refreshToken>/', views.upload, name='upload'),
]
