import re
import uuid

from datetime import datetime
from django.conf import settings

from kolibri.auth.models import FacilityUser
from ..models import PhoneToUsernameMapping


def normalize_phone_number(phone):
    """Remove everything except digits from the phone number string."""
    return re.sub("\D", "", str(phone))


def get_usernames(phone):
    """Look up the usernames associated with this phone number."""
    
    # normalize the phone number to only digits
    phone = normalize_phone_number(phone)

    # look up all of the associated usernames
    return list(PhoneToUsernameMapping.objects.filter(phone=phone).values_list("username", flat=True))


def create_new_username(phone):
    uuidval = uuid.uuid4().hex
    old_usernames = get_usernames(phone)
    if old_usernames:
        # keep the first 10 characters the same so we can see which users are from the same phone number
        username = old_usernames[0][:10] + uuidval[:20]
    else:
        # no existing users, so just use a random id as username
        username = uuidval[:30]
    PhoneToUsernameMapping.objects.create(username=username, phone=phone)
    return username


def get_facility_users(phone):

    # get the list of usernames associated with the phone number
    usernames = get_usernames(phone)

    return FacilityUser.objects.filter(username__in=usernames)


def get_phone_number(username):
    """Look up the phone number for a specific username, from the reverse lookup database."""
    try:
        return PhoneToUsernameMapping.objects.get(username=username).phone
    except PhoneToUsernameMapping.DoesNotExist:
        return None
