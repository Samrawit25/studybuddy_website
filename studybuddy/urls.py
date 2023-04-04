from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='landingPage'),
    path('logout/', views.logout_uva_user, name='logout'),
    path('registration/', views.verify, name='registration'),
    path('homepage/', views.homepage, name='homePage'),
    path('profile/', views.profile, name='profilePage'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

