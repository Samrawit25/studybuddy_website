from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='landingPage'),
    path('homepage/', views.homepage, name='homePage'),
    path('profile/', views.profile, name='profilePage'),
]
