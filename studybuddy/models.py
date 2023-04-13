from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, unique=True)
    computing_id = models.CharField(max_length=20, null=True, unique=True)
    gender = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='/profile_pictures/default_profile_picture.jpg')
    phone_number = models.IntegerField(null=True)
    department = models.CharField(max_length=255, null=True)
    current_year = models.CharField(max_length=20, null=True)
    gender_visible = models.BooleanField(default=False)
    phone_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'First name: {self.user.first_name}, Last name: {self.user.last_name}'

class Course(models.Model):
    course_number = models.CharField(max_length=255, null=True, unique=True)
    course_section = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    units = models.CharField(max_length=255, null=True)
    catalog_number = models.CharField(max_length=255, null=True)
    instructor_first_name = models.CharField(max_length=255, null=True)
    instructor_last_name = models.CharField(max_length=255, null=True)
    instructor_email = models.CharField(max_length=255, null=True)


class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    studyCourse = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    publish_date = models.DateField(null=True)
    studyPreference = models.CharField(max_length=255, null=True)
    # date_added = models.DateTimeField(primary_key=True, default=now, blank=False)


class StudyBuddy(models.Model):
    post_reference = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    publish_date = models.DateField(null=True)


class StudyGroup(models.Model):
    post_reference = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    publish_date = models.DateField(null=True)
