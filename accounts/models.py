from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith("pbkdf2_"):
            # Only hash if it's a new user or a raw password was set
            self.set_password(self.password)
        super().save(*args, **kwargs)
