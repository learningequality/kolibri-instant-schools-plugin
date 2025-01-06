# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from kolibri.deployment.default.settings.dev import *  # noqa

USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
ALLOW_CERTIFICATE_PUSHING = False 
