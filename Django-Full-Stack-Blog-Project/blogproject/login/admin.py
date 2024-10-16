from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserInLine(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = "Custom Users"


class UserAdmin(BaseUserAdmin):
    inlines = [CustomUserInLine]    


admin.site.unregister(User)
admin.site.register(User, UserAdmin)