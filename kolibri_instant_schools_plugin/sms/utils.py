import os
from twilio.rest import Client
from django.core.urlresolvers import reverse
import logging as logger

from ..auth.mapping import normalize_phone_number

logging = logger.getLogger("kolibri")

SMS_MESSAGE_TEMPLATE = os.environ.get("SMS_MESSAGE_TEMPLATE")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_MESSAGING_SID = os.environ.get("TWILIO_MESSAGING_SID")

required_env_vars = [
    ("SMS_MESSAGE_TEMPLATE", SMS_MESSAGE_TEMPLATE),
    ("TWILIO_SID", TWILIO_SID),
    ("TWILIO_AUTH_TOKEN", TWILIO_AUTH_TOKEN),
    ("TWILIO_MESSAGING_SID", TWILIO_MESSAGING_SID),
]

env_var_errors = False

for name, value in required_env_vars:
    if not value:
        env_var_errors = True
        logging.error("{} is not set".format(name))

if env_var_errors:
    class ConfigurationError(Exception):
        pass
    raise ConfigurationError("Twilio is not configured properly. The service will not start until this is resolved.")


def send_password_reset_link(prefix, phone, token, baseurl):

    phone = normalize_phone_number(phone)
    baseurl = baseurl.rstrip("/")
    endpointurl = reverse("kolibri:kolibri_instant_schools_plugin:instant_schools_auth")
    path = "{endpointurl}{phone}/{token}".format(endpointurl=endpointurl, token=token, phone=phone)


    url = "{baseurl}/{path}".format(
        baseurl=baseurl, path=path
    )

    send_message(prefix, phone, SMS_MESSAGE_TEMPLATE.format(url=url))


def send_message(prefix, phone, message):

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
      messaging_service_sid=TWILIO_MESSAGING_SID,
      to="{}{}".format(prefix, phone),
      body=message,
    )

    print(message.sid)
