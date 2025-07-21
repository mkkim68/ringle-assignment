from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, MembershipType

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("name", "role", "company")}),
    )
    list_display = BaseUserAdmin.list_display + ("name", "role", "company")
    list_filter = BaseUserAdmin.list_filter + ("role", "company")

admin.site.register(Company)
admin.site.register(MembershipType)