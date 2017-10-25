from django.conf import settings

from kolibri.auth.models import Facility
from kolibri.auth.api import SignUpViewSet

from .hashing import get_hash_value


class PhoneNumberSignUpViewSet(SignUpViewSet):

    def extract_request_data(self, request):
        data = super(PhoneNumberSignUpViewSet, self).extract_request_data(request)
        if getattr(settings, "USE_PHONE_NUMBER_HASHING", False):
            data["username"] = get_hash_value(data["username"])
        return data
