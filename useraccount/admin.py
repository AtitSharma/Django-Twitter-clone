from django.contrib import admin
# from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from useraccount.models import Profile

# Register your models here.


# admin.site.register(User)
User=get_user_model()

@admin.register(User)
class CustomiseAdmin(UserAdmin):
    pass




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","contact","address")
