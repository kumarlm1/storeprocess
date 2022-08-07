from django.contrib import admin
from .models import NewUser, Folder, File,Problem
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
    exclude = ('username',)
    fieldsets = (
        (None, {"fields": ("email", "user_name", "first_name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_verified_email")}),
        ("Personal", {"fields": ("about",)}),
    )


class UserAdminConfigFolder(admin.ModelAdmin):

    ordering = ("-updated",)
    list_filter = ('created', 'name')
    list_display = ('user', 'name', 'created', 'updated')
    fieldsets = (
        (None, {"fields": ("user",
                           "name",
                           )}),


    )
    readonly_fields = ['created', 'updated']


class UserAdminConfigFiles(admin.ModelAdmin):

    ordering = ("-updated",)
    list_filter = ('updated', 'filename')
    list_display = ('user', 'folder', 'filename', 'updated')
    fieldsets = (
        (None, {"fields": ("user",
                           "folder",
                           "filename",
                           )}),


    )
    readonly_fields = ['updated']
class UserAdminConfigProblem(admin.ModelAdmin):

    
   
    list_display = ('file_id','data')
    fieldsets = (
        (None, {"fields": ("data",
                        
                           "file_id",
                           )}),


    )
   

admin.site.register(NewUser, UserAdminConfig)

admin.site.register(Folder, UserAdminConfigFolder)
admin.site.register(File, UserAdminConfigFiles)
admin.site.register(Problem,UserAdminConfigProblem)
