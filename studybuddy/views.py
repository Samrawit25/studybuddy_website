from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import PostForm, ProfileUpdateForm
from django.contrib import messages
import requests
from django.views.generic import UpdateView
from django.db.models import Q
from django.templatetags.static import static


def index(request):
    return render(request, "login.html", {})



def logout_uva_user(request):
    """
        This function will log the user out of our application then perform a complete logout of their Google account.
        This is the only way to force reauthentication when they revisit our site.
    """
    logout(request)

    # Redirect the user to the Google URL to log them out of their Google account
    return redirect('https://www.google.com/accounts/Logout')


@login_required
def verify(request):
    try:
        user_profile = request.user.profile

    except:
        # Throw an exception if the current user does not have a Profile.
        # Redirects them to registration page to complete their profile

        if request.method == 'POST':
                # Create a Student Profile
                entered_profile_picture = request.POST['profile_picture']
                entered_date_of_birth = request.POST['age']
                entered_computing_id = request.POST['computing_id'].strip()
                entered_major = request.POST['major'].strip()
                entered_year = request.POST['current_year']

                new_student = Profile(user=request.user, email=request.user.email,
                                      profile_picture=f'profile_picture/{entered_profile_picture}',
                                      computing_id=entered_computing_id,
                                      date_of_birth=entered_date_of_birth,
                                      department=entered_major,
                                      current_year=entered_year)
                new_student.save()
                return redirect('homePage')

        luthers_list_API_response = requests.get(
            "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH"
            ".FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232").json()[
            "subjects"]

        all_dept = []

        for dept in luthers_list_API_response:
            all_dept.append(dept["subject"])

        context = {"uva_departments": all_dept,}

        return render(request, "studybuddy/registration.html", context)
        # else:
        #     return render(request, "login.html", {})

    else:
        return redirect('homePage')



@login_required
def homepage(request):
    try:
        user_profile = request.user.profile
    except:
        return redirect('verification')


    luthers_list_API_response = requests.get(
        "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH"
        ".FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232").json()[
        "subjects"]

    all_dept = []

    for dept in luthers_list_API_response:
        all_dept.append(dept["subject"])

    #for search
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            all_posts = Post.objects.filter(
                Q(studyCourse__icontains=query)|
                Q(studyPreference__icontains=query)|
                Q(description__icontains=query)
            ).distinct()
        else:
            all_posts = Post.objects.all()

    context = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "computing_id": request.user.profile.computing_id,
        "major": request.user.profile.department,
        "available_posts": all_posts,
        "uva_departments": all_dept,
    }

    return render(request, "studybuddy/homepage.html", context)


@login_required
def userPost(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            form = PostForm()
            messages.success(request, "Successfully created")
            return redirect('homePage')

    return render(request, 'studybuddy/post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated")
            return redirect('profilePage')
    else:
        form = PostForm(instance=post)

    return render(request, 'studybuddy/editUserPost.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Successfully deleted")
        return redirect('profilePage')

    return render(request, 'studybuddy/deleteUserPost.html', {'post': post})


@login_required
def profile(request):
    all_posts = Post.objects.filter(owner=User.objects.get(email=request.user.email))
    context = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "computing_id": request.user.profile.computing_id,
        "profile_pic": request.user.profile.profile_picture.url,
        "major": request.user.profile.department,
        "all_posts": all_posts,
        "date_of_birth": request.user.profile.date_of_birth,
        "phone_number": request.user.profile.phone_number,
    }
    return render(request, 'studybuddy/profilePage.html', context)


@login_required
def editProfilePage(request):
    if request.method == 'POST':
        pro_form = ProfileUpdateForm(request.POST, request.FILES,
                                     instance=request.user.profile)

        # save the edited profile info
        if pro_form.is_valid():
            pro_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profilePage')

    else:
        pro_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'pro_form': pro_form
    }
    return render(request, 'studybuddy/editProfile.html', context)


@login_required
def contact(request):
    return render(request, 'base.html', {})
