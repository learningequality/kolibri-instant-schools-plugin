import uuid

from django.db import models
from django.utils import timezone
from kolibri.core.auth.models import FacilityUser
from django.contrib.auth.hashers import make_password

TOKEN_VALIDITY_MINUTES = 60 * 48  # tokens last for 48 hours
SALT = "1a8e928ae600405b9c1acef123502fb1"


class AboutFAQ(models.Model):
    html = models.TextField()
    kind = models.TextField(choices=(("FAQ", "FAQ"), ("About", "About")))

    class Meta:
        app_label = "kolibri_instant_schools_plugin"


class PhoneHashToUsernameMapping(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    hash = models.CharField(max_length=150)

    def set_phone(self, phone):
        self.hash = make_password(phone, salt=SALT)

    @classmethod
    def get_users(cls, phone, password):
        users = FacilityUser.objects.filter(
            username__in=cls.objects.filter(hash=make_password(phone, salt=SALT)).values_list("username", flat=True)
        )
        for user in users:
            if not user.check_password(password):
                raise Exception("Incorrect password")
        return users

    class Meta:
        app_label = "kolibri_instant_schools_plugin"


class PasswordResetToken(models.Model):
    token = models.CharField(max_length=12, primary_key=True)
    phone = models.CharField(max_length=20, db_index=True)
    created = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False)
    used = models.BooleanField(default=False)

    class Meta:
        app_label = "kolibri_instant_schools_plugin"

    @classmethod
    def generate_new_token(cls, phone):
        token = uuid.uuid4().hex[:12]
        return cls.objects.create(phone=phone, token=token)

    def is_valid(self):
        if self.expired or self.used:
            return False
        if (timezone.now() - self.created).total_seconds() / 60 > TOKEN_VALIDITY_MINUTES:
            self.expired = True
            self.save()
            return False
        return True

    def use_token(self):
        if not self.is_valid():
            raise Exception("Token is not valid!")
        self.used = True
        self.save()
