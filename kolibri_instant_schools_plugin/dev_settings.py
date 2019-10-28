# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from kolibri_instant_schools_plugin.instant_schools_settings import *  # noqa

# copied from kolibri.deployment.settings.dev
INSTALLED_APPS += ["rest_framework_swagger"]  # noqa
INTERNAL_IPS = ["127.0.0.1"]
ROOT_URLCONF = "kolibri.deployment.default.dev_urls"
DEVELOPER_MODE = True
# Create a dummy cache for each cache
CACHES = {
    key: {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}
    for key in CACHES.keys()  # noqa F405
}

# so user won't be logged out during development
SESSION_COOKIE_AGE = 10000000
