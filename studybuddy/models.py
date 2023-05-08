from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, unique=True)
    computing_id = models.CharField(max_length=20, null=True, unique=True)
    gender = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='/profile_pictures/default_pic.jpg')
    phone_number = models.IntegerField(null=True)
    department = models.CharField(max_length=255, null=True)
    current_year = models.CharField(max_length=20, null=True)
    gender_visible = models.BooleanField(default=False)
    phone_visible = models.BooleanField(default=False)

    def __str__(self):
        return f'First name: {self.user.first_name}, Last name: {self.user.last_name}'


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    studyCourse = models.CharField(max_length=255, null=True)
    studyPreference = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=400, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    # date_added = models.DateTimeField(primary_key=True, default=now, blank=False)


class StudyBuddy(models.Model):
    post_reference = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    publish_date = models.DateField(null=True)


class StudyGroup(models.Model):
    post_reference = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    publish_date = models.DateField(null=True)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    # Make objects sortable using list.sort()

    def __lt__(self, dm):
        return self.date_sent < dm.date_sent


select_mode_of_contact = (
    ("email", "E-Mail"),
    ("phone", "Phone"),
)
select_question_categories = (
    ("certification", "Certification"),
    ("interview", "Interview"),
    ("material", "Material"),
    ("access_duration","Access and Duration"),
    ("other", "Others"),
)

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    mode_of_contact = models.CharField('Contact by', max_length=50, choices=select_mode_of_contact, default='email')
    question_categories = models.CharField('How can we help you?', max_length=50, choices=select_question_categories, default='certification')
    message = models.TextField(max_length=3000)
    archived = models.BooleanField(default=False)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.email

