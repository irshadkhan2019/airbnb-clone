from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "english"
    LANGUAGE_HINDI = "hindi"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_HINDI, "Hindi"))

    CURRENCY_USD = "usd"
    CURRENCY_INR = "inr"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_INR, "INR"))

    bio = models.TextField(default="", blank=True)
    avatar = models.ImageField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, blank=True, max_length=10)
    currency = models.CharField(choices=CURRENCY_CHOICES, blank=True, max_length=3)
    superhost = models.BooleanField(default=False)
    birthdate = models.DateField(blank=True, null=True)
