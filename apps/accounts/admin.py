from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser
from projects.admin import CapacityInline


class CustomUserAdmin(UserAdmin):
    readonly_fields = ("updated_at",)
    model = CustomUser
    inlines = [CapacityInline]


admin.site.register(CustomUser, CustomUserAdmin)
