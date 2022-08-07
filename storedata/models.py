from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as g_l

# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(
            email=email, user_name=user_name, first_name=first_name, **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, password, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Super User must be staff")

        return self.create_user(email, user_name, first_name, password, **kwargs)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified_email = models.BooleanField(
        g_l("Whether User is verified email address"), default=False
    )

    objects = CustomAccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "first_name"]

    def __str__(self):
        return f"{self.user_name} {self.email}"


class Folder(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['updated']


class File(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=150, blank=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['updated']

class Problem(models.Model):
    file_id = models.ForeignKey(File,on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return self.file_id
