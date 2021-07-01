from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.http import base36_to_int, int_to_base36
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from six import text_type
from .models import NewUser


class VerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        return text_type(text_type(user.is_verified_email) + text_type(timestamp))

    def _make_token_with_timestamp(self, user, timestamp):

        ts_b36 = int_to_base36(timestamp)

        hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp),
        ).hexdigest()[::]
        return "%s-%s" % (ts_b36, hash)


Verificationtoken = VerificationTokenGenerator()


def Send_Email(to, html_content, text_content, subject):
    email = EmailMultiAlternatives(subject, text_content, to=to)
    email.attach_alternative(html_content, "text/html")
    email.send()


def Verification_Mail(request):
    user = NewUser.objects.get(email=request.user.email)
    uid = urlsafe_base64_encode(force_bytes(user.email))
    domain = get_current_site(request).domain
    link = (
        domain
        + reverse("storedata:activate",
                  kwargs={"uid": uid, "token": Verificationtoken.make_token(user)})
    )
    print(link)
    html_content = render_to_string(
        'storedata/MailTemplate/mail_body.html', {'link': link})
    text_content = render_to_string(
        'storedata/MailTemplate/mail_body.txt', {'user.user_name': user.user_name, 'link': link})
    Send_Email(to=[user.email], html_content=html_content,
               text_content=text_content, subject="Verify Email")


def Password_reset_Mail(request, email):
    user = NewUser.objects.get(email=email)
    uid = urlsafe_base64_encode(force_bytes(user.email))
    domain = get_current_site(request).domain
    link = (
        domain
        + reverse("storedata:reset",
                  kwargs={"uid": uid, "token": Verificationtoken.make_token(user)})
    )
    html_content = render_to_string(
        'storedata/MailTemplate/mail_body.html', {'link': link})
    text_content = render_to_string(
        'MailTemplate/mail_body.txt', {'user.user_name': user.user_name, 'link': link})
    Send_Email(to=[user.email], html_content=html_content,
               text_content=text_content, subject="Password Reset")
