from django.contrib import admin
from .models import NewUser, Folder
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdminConfig(UserAdmin):

    ordering = ("-start_date",)
    list_display = (
        "email",
        "user_name",
        "first_name",
        "is_active",
        "is_verified_email",
    )
    fieldsets = (
        (None, {"fields": ("email", "user_name", "first_name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_verified_email")}),
        ("Personal", {"fields": ("about",)}),
    )


class UserAdminConfigFolder(admin.ModelAdmin):

    ordering = ("-updated",)
    list_filter = ('created', 'name')
    list_display=('user','name','created','updated')
    fieldsets = (
        (None, {"fields": ("user",
                           "name",
                           )}),


    )
    readonly_fields = ['created', 'updated']


admin.site.register(NewUser, UserAdminConfig)

admin.site.register(Folder, UserAdminConfigFolder)
