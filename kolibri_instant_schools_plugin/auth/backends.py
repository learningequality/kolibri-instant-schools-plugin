"""
Implements custom auth backend for FacilityUser that hashes the phone number before checking against DB.
"""

from kolibri.auth.backends import FacilityUserBackend

from .hashing import get_hash_value


class PhoneNumberFacilityUserBackend(FacilityUserBackend):
    """
    A class that implements authentication for FacilityUsers, with hashed phone numbers as username.
    """

    def authenticate(self, username=None, password=None, facility=None):
        """
        Authenticates the user if the credentials correspond to a FacilityUser for the specified Facility.

        :param username: a string, in the form of a phone number
        :param password: a string
        :param facility: a Facility
        :return: A FacilityUser instance if successful, or None if authentication failed.
        """
        return super(PhoneNumberFacilityUserBackend, self).authenticate(
            username=get_hash_value(username),
            password=password,
            facility=facility,
        )
