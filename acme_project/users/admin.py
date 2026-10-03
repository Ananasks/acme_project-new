from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('bio',)}),
    )
