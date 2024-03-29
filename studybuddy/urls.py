from django.contrib import admin
from django.urls import path, include
# from .views import editUserPost
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
    path('post/delete/<int:post_id>/', views.delete_post, name='deletePost'),
    path('profile/edit/<int:post_id>/', views.edit_post, name='editPost'),
    path('homepage/send_message/<int:recipient_id>/', views.send_message, name='sendMessage'),
    path('message/', views.messages, name='message'),
    path('representative', views.list_messages, name='representativePortal'),
    path('contact/', views.contact, name='contact'),
    path('contact/thanks', views.contact, name='contact_thankyou'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

