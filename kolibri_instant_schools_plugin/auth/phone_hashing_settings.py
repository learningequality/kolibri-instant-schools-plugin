from kolibri.deployment.default.settings.base import *

AUTHENTICATION_BACKENDS = ['kolibri.auth.backends.DeviceOwnerBackend', 'kolibri_instant_schools_plugin.auth.backends.PhoneNumberFacilityUserBackend']

USE_PHONE_NUMBER_HASHING = True
