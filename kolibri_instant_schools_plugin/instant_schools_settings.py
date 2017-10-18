from kolibri.deployment.default.settings.base import *

USE_PHONE_NUMBER_MAPPING = True

DATABASES["instant_schools"] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(KOLIBRI_HOME, 'instant_schools.db'),
    'OPTIONS': {
        'timeout': 100,
    }
}

DATABASE_ROUTERS = ["kolibri_instant_schools_plugin.db_router.InstantSchoolsRouter"]

if "kolibri_instant_schools_plugin" not in INSTALLED_APPS:
    INSTALLED_APPS += ["kolibri_instant_schools_plugin"]
