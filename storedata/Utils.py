from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

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
