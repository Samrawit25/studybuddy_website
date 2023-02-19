from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


posts = [
    {
        'Name': 'Tom',
        'Major': 'Computer Science',
        'Course': 'CS 2150',
        'Description': 'looking for study partner for Cs 2150'
    },
    {
        'Name': 'Sam',
        'Major': 'Math',
        'Course': 'APMA 3100',
        'Description': 'looking for study partner for probability course'
    }
]
def index(request):
    return render(request, "studybuddy/landingpage.html", {})


def homepage(request):
    context = {
        'posts': posts
    }
    return render(request, "studybuddy/homepage.html", context)


def profile(request):
    return render(request, "studybuddy/profilepage.html", {})
