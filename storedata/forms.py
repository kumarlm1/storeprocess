from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NewUser


# Create your views here.


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = NewUser
        fields = ("user_name", "first_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.user_name = self.cleaned_data["user_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PasswordResetForms(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ("password1", "password2")

    def save(self, commit=True):
        user = super(PasswordResetForms, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmailForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = NewUser
        fields = ("email", "password1", "password2")


class CommentForm(forms.Form):
    name = forms.CharField(label='Folder Name')
