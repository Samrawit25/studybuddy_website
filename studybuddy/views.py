from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
import requests
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
                entered_date_of_birth = request.POST['age']
                entered_computing_id = request.POST['computing_id'].strip()
                entered_major = request.POST['major'].strip()
                entered_year = request.POST['current_year']

                new_student = Profile(user=request.user, email=request.user.email,
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

    all_posts = Post.objects.all()

    context = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "computing_id": request.user.profile.computing_id,
        "major": request.user.profile.department,
        "available_posts": all_posts,
    }

    return render(request, "studybuddy/homepage.html", context)


@login_required
def userPost(request):
    if request.method == "POST":
        entered_study_course = request.POST.get('studyCourse')
        entered_study_preference = request.POST['studyPreference']
        entered_comment = request.POST.get('description')
        entered_publish_date = request.POST['publish_date']

        # entered_trade_option = request.POST['trade_options']
        # entered_comment = request.POST['comments']
        # entered_isbn = request.POST['isbn'].strip()
        # entered_book_cover = request.POST['book_cover']
        # full_author_name = request.POST['author_name'].strip()
        # entered_author_first_name = full_author_name.split()[0]


        # Create a new post
        # The post does not exist in the post table, so first create an instance of it:

        new_post = Post(studyCourse=entered_study_course,
                            studyPreference=entered_study_preference,
                            description=entered_comment,
                            publish_date=entered_publish_date)
        new_post.save()

        # Create an AvailableBook that references the newly created Book
        new_available_post = Post()
        # new_available_book_lisitng.book_reference = new_book
        # new_available_post.
        new_available_post.owner = Profile.objects.get(email=request.user.email)
        new_available_post.study_course = entered_study_course
        new_available_post.study_preference = entered_study_preference
        new_available_post.description = entered_comment
        new_available_post.save()

        return redirect('homePage')


    context = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "computing_id": request.user.profile.computing_id,
        "major": request.user.profile.department,
    }

    return render(request, 'studybuddy/post.html', context)



@login_required
def profile(request):

    # Pass ALL the logged in student's information to the template
    # logged_in_student = Profile.objects.get(email=request.user.email)

    if request.method == "POST":
        # Change template if user wants to update personal information
        try:
            request.POST['edit_profile_identifier']
        except:
            pass
        else:
            edit_profile_information = True

        # Handle the POST request to update personal information
        try:
            request.POST['edit_profile_confirmation_identifier']
        except:
            pass
        else:

            update_picture = request.POST['picture_status']
            update_major = request.POST['major_status']
            update_year = request.POST['year_status']
            update_phone_number = request.POST['phone_number_status']
            update_gender_visibility = request.POST['gender_visibility_status']
            update_phone_visibility = request.POST['phone_visibility_status']

            if update_picture == "true":
                new_picture = request.FILES['user_profile_picture']
            else:
                new_picture = Profile.objects.get(
                    email=request.user.email).profile_picture

            if update_major == "true":
                new_major = request.POST['major']
            else:
                new_major = Profile.objects.get(email=request.user.email).department

            if update_year == "true":
                new_year = request.POST['current_year']
            else:
                new_year = Profile.objects.get(email=request.user.email).current_year

            if update_phone_number == "true":
                new_phone_number = request.POST['phone_number']
            else:
                new_phone_number = Profile.objects.get(
                    email=request.user.email).phone_number

            if update_gender_visibility == "true":
                new_gender_visibility = request.POST['gender_visibility']

            else:
                new_gender_visibility = Profile.objects.get(
                    email=request.user.email).gender_visible

            if update_phone_visibility == "true":
                new_phone_visibility = request.POST['phone_visibility']

            else:
                new_phone_visibility = Profile.objects.get(
                    email=request.user.email).phone_visible

            logged_in_user = Profile.objects.get(email=request.user.email)
            logged_in_user.profile_picture = new_picture
            logged_in_user.phone_number = new_phone_number
            logged_in_user.department = new_major
            logged_in_user.current_year = new_year
            logged_in_user.gender_visible = new_gender_visibility
            logged_in_user.phone_visible = new_phone_visibility
            logged_in_user.save(
                update_fields=['profile_picture', 'current_year', 'phone_visible',
                               'gender_visible', 'department', 'phone_number'])

            return redirect("profilePage")


    # if edit_profile_information:
    #     context = {
    #         'student': logged_in_student
    #     }
    #     return render(request, 'studybuddy/edit_profilePage_information.html', context)

    else:
        return render(request, 'studybuddy/profilePage.html', {})


def contact(request):
    return render(request, 'base.html', {})
