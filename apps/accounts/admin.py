from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from simple_history.admin import SimpleHistoryAdmin
from .models import CustomUser


# class CustomUserAdmin(UserAdmin, SimpleHistoryAdmin):
class CustomUserAdmin(UserAdmin):
    readonly_fields = ("updated_at",)
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
