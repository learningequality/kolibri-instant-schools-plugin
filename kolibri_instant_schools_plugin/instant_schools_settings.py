# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
if(os.environ("KUBERNETES_PORT")):
    from kolibri.deployment.default.settings.cloud_kolibri_settings import *
else:
    from kolibri.deployment.default.settings.base import *

OLD_DB_PATH = os.path.join(conf.KOLIBRI_HOME, 'db.sqlite3')
OLD_HASH_DB_PATH = os.path.join(conf.KOLIBRI_HOME, 'phonehashreverselookup.db')

DATABASES["default"]["NAME"] = os.path.join(conf.KOLIBRI_HOME, 'instant_schools_primary.sqlite3')

LANGUAGES = [
    ('en', 'English'),
    ('sw-tz', 'Kiswahili'),
    ('fr-fr', 'Français'),
    ('pt-br', 'Português'),
]

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ALLOW_CERTIFICATE_PUSHING = True 

