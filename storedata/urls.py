from django.urls import path, include
from . import views
from django_email_verification import urls as email_urls
from django.contrib.auth import views as auth_views

app_name = "storedata"
urlpatterns = [
    path("", views.home, name="homepage"),
    path("register", views.register_request, name="register"),
    path(
        "login",
        views.login_request,
        name="login",
    ),
    path(
        "logout",
        views.logout_request,
        name="logout",
    ),
    path(
        "verify",
        views.verify_mail,
        name="verify",
    ),
    path(
        "reset",
        views.email_pass_reset,
        name="email_pass_reset",
    ),
    path(
        "reset_pass",
        views.reset_password__request,
        name="pass_reset",
    ),
    path("email/", include(email_urls)),
    path("activate/<uid>/<token>", views.domains, name="activate"),
    path("reset/<uid>/<token>", views.password_reset, name="reset"),
    path('sc',views.screenshot)
]
