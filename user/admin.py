from django.contrib import admin
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','adress','phone_number','city','country','image_tag']

admin.site.register(UserProfile, UserProfileAdmin)

