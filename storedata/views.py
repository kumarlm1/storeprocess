from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.template import Context
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import NewUser, Folder
from .forms import NewUserForm, PasswordResetForms, EmailForm, CommentForm
from .Utils import Verificationtoken, Verification_Mail, Password_reset_Mail



@csrf_exempt
@login_required(login_url="/login")
def home(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Folder.objects.update_or_create(
                name=form.cleaned_data.get('name'), user=request.user)
    else:
        form = CommentForm()
    template_name = "storedata/home.html"
    folder = Folder.objects.filter(user=request.user).order_by('-updated')
    return render(request=request, template_name=template_name, context={'folder': folder, 'form': form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("storedata:homepage")
    form = NewUserForm
    return render(
        request=request,
        template_name="storedata/regist.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("storedata:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="storedata/signin.html",
        context={"login_form": form},
    )


def logout_request(request):
    logout(request)
    return redirect("storedata:homepage")


def verify_mail(request):
    Verification_Mail(request=request)
    return JsonResponse("send", safe=False)


def verify_mail_reset(request, email):
    Password_reset_Mail(request=request, email=email)
    return JsonResponse("send", safe=False)


def domains(request, uid, token):
    try:
        id = force_text(urlsafe_base64_decode(uid))
        print(id)
        user = NewUser.objects.get(email=id)
        if not Verificationtoken.check_token(user, token):
            return HttpResponse(
                "<html><body><h1>Already Registered or Timeout</h1></body></html>"
            )
        if not user.is_verified_email:
            user.is_verified_email = True
            user.save()

        return redirect("storedata:homepage")
    except Exception as e:
        print(e)

        return HttpResponse("<html><body><h1>Invalid Code</h1></body></html>")


def email_pass_reset(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        print("entered")
        print("entered  sd")
        email = form.data.get("email")
        verify_mail_reset(request=request, email=email)
        return HttpResponse("sennnt.....check mail")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = EmailForm
    return render(
        request=request,
        template_name="storedata/reset.html",
        context={"password_reset_form": form},
    )


def password_reset(request, uid, token):
    try:
        id = force_text(urlsafe_base64_decode(uid))
        print(id)
        user = NewUser.objects.get(email=id)
        if Verificationtoken.check_token(user, token):
            if request.method == "POST":
                form = PasswordResetForms(request.POST)
                password = form.data.get("password")
                user = NewUser.objects.get(email=request.session.get("email"))
                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("storedata:homepage")
            form = PasswordResetForms
            return render(
                request=request,
                template_name="storedata/pass_reset.html",
                context={"password_reset_form": form},
            )

            return redirect("storedata:pass_reset")
    except Exception as e:
        print(e)

        return HttpResponse("<html><body><h1>Invalid Code</h1></body></html>")


def reset_password__request(request):
    if request.method == "POST":
        form = PasswordResetForms(request.POST)
        password = form.data.get("password")
        user = NewUser.objects.get(email=request.session.get("email"))
        user.set_password(password)
        user.save()
        login(request, user)
        messages.success(request, "Registration successful.")
        return redirect("storedata:homepage")
    form = PasswordResetForms
    return render(
        request=request,
        template_name="storedata/pass_reset.html",
        context={"password_reset_form": form},
    )
