from django.db import models


class PhoneToUsernameMapping(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    phone = models.CharField(max_length=20, db_index=True)
