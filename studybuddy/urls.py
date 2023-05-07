from django.contrib import admin
from django.urls import path, include
# from .views import CreatePostView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='landingPage'),
    path('logout/', views.logout_uva_user, name='logout'),
    path('registration/', views.verify, name='registration'),
    path('homepage/', views.homepage, name='homePage'),
    path('profile/', views.profile, name='profilePage'),
    path('profile/edit', views.editProfilePage, name='editProfile'),
    path('homepage/post/', views.userPost, name='post'),
    path('contact', views.contact, name='contact'),

    # path('post/new/', CreatePostView.as_view(), name='postCreate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

