from django.contrib import admin
from .models import Profile, Post, StudyBuddy, StudyGroup

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(StudyBuddy)
admin.site.register(StudyGroup)
