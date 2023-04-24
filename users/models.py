import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import reverse


class User(AbstractUser):
    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "english"
    LANGUAGE_HINDI = "hindi"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_HINDI, "Hindi"))

    CURRENCY_USD = "usd"
    CURRENCY_INR = "inr"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_INR, "INR"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "Github"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, _("Email")),
        (LOGIN_GITHUB, _("Github")),
    )

    bio = models.TextField(default="", blank=True)
    avatar = models.ImageField(blank=True, upload_to="avatars")
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICES, max_length=10, blank=True
    )
    language = models.CharField(
        choices=LANGUAGE_CHOICES, blank=True, max_length=10, default=LANGUAGE_ENGLISH
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, blank=True, max_length=3, default=CURRENCY_INR
    )
    superhost = models.BooleanField(default=False)
    birthdate = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        max_length=40, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                _("Verify Airbnb Account"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
