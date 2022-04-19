import re
import uuid

from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import make_password

from kolibri.core.auth.models import FacilityUser
from ..models import PhoneHashToUsernameMapping, SALT


def normalize_phone_number(phone):
    """Remove everything except digits and "+" symbol from the phone number string."""
    return re.sub("[^\d\+]", "", str(phone))

def hash_phone(phone):
    """Hash a phone number, and return the hashed value."""
    return make_password(normalize_phone_number(phone), salt=SALT)

def get_usernames(hashed_phone):
    """Look up the usernames associated with this phone hash."""

    # look up all of the associated usernames
    return list(PhoneHashToUsernameMapping.objects.filter(hash=hashed_phone).values_list("username", flat=True))

def create_new_username(phone_number):
    hashed_phone = hash_phone(phone_number)
    old_usernames = get_usernames(hashed_phone)
    if old_usernames:
        # keep the first 10 characters the same so we can see which users are from the same phone number
        username = old_usernames[0][:10] + uuid.uuid4().hex[:20]
    else:
        # no existing users, so just use a random id as username
        username = uuid.uuid4().hex[:30]
    PhoneHashToUsernameMapping.objects.create(username=username, hash=hashed_phone)
    return username

def get_facility_users(phone):

    # get the list of usernames associated with the phone number
    usernames = get_usernames(phone)

    return FacilityUser.objects.filter(username__in=usernames)

def get_hash(username):
    """Look up the hash for a specific username, from the reverse lookup database."""
    try:
        return PhoneHashToUsernameMapping.objects.get(username=username).hash
    except PhoneHashToUsernameMapping.DoesNotExist:
        return None

