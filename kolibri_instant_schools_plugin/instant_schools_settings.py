# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from kolibri.deployment.default.settings.base import *

if "kolibri_instant_schools_plugin" not in INSTALLED_APPS:
    INSTALLED_APPS += ["kolibri_instant_schools_plugin"]

OLD_DB_PATH = os.path.join(conf.KOLIBRI_HOME, 'db.sqlite3')
OLD_HASH_DB_PATH = os.path.join(conf.KOLIBRI_HOME, 'phonehashreverselookup.db')

DATABASES["default"]["NAME"] = os.path.join(conf.KOLIBRI_HOME, 'instant_schools_primary.sqlite3')

DATABASES["instant_schools"] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(conf.KOLIBRI_HOME, 'instant_schools.db'),
    'OPTIONS': {
        'timeout': 100,
    }
}

DATABASE_ROUTERS = ["kolibri_instant_schools_plugin.db_router.InstantSchoolsRouter"]


LANGUAGES = [
    ('en', 'English'),
    ('sw-tz', 'Kiswahili'),
    ('fr-fr', 'Français'),
    ('pt-pt', 'Português'),
]
