from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.template import Context
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


# Create your views here.
from .models import NewUser
from .forms import NewUserForm, PasswordResetForms, EmailForm
from .Utils import Verificationtoken


@login_required(login_url="/login")
def home(request):
    template_name = "storedata/home.html"
    return render(request=request, template_name=template_name)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("storedata:homepage")
    form = NewUserForm
    return render(
        request=request,
        template_name="storedata/register.html",
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
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("storedata:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="storedata/login.html",
        context={"login_form": form},
    )


def logout_request(request):
    logout(request)
    return redirect("storedata:homepage")


def send(to, name):
    subject = "subject"
    content = "This is test content for {name}"
    html_content = f"<p>This is <strong>test</strong> content for {name} </p>".format(
        name=name
    )
    email = EmailMultiAlternatives(subject, content, to=to)
    email.attach_alternative(html_content, "text/html")
    email.send()


def verify_mail(request):
    user = NewUser.objects.get(email=request.user.email)
    uid = urlsafe_base64_encode(force_bytes(user.email))
    domain = get_current_site(request).domain
    tokens = Verificationtoken.make_token(user)
    link = (
        "http://"
        + domain
        + reverse("storedata:activate", kwargs={"uid": uid, "token": tokens})
    )
    print(link)
    send([user.email], link)

    messages.info(request, f"You are now logged in as {user.email}.")
    return JsonResponse("send", safe=False)


def verify_mail_reset(request, email):
    user = NewUser.objects.get(email=email)
    uid = urlsafe_base64_encode(force_bytes(user.email))
    domain = get_current_site(request).domain
    tokens = Verificationtoken.make_token(user)
    link = (
        "http://"
        + domain
        + reverse("storedata:reset", kwargs={"uid": uid, "token": tokens})
    )
    send([user.email], link)

    messages.info(request, f"You are now logged in as {user.email}.")
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
        messages.error(request, "Unsuccessful registration. Invalid information.")
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
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = PasswordResetForms
    return render(
        request=request,
        template_name="storedata/pass_reset.html",
        context={"password_reset_form": form},
    )
