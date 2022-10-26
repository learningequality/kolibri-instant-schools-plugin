import os
from twilio.rest import Client
from django.core.urlresolvers import reverse

from ..auth.mapping import normalize_phone_number

SMS_MESSAGE_TEMPLATE = os.environ.get("SMS_MESSAGE_TEMPLATE")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_MESSAGING_SID = os.environ.get("TWILIO_MESSAGING_SID")

if not (TWILIO_SID and TWILIO_AUTH_TOKEN and TWILIO_MESSAGING_SID and SMS_MESSAGE_TEMPLATE):
    class ConfigurationError(Exception):
        pass
    raise ConfigurationError("Twilio not configured properly. SMS password reset will not work until Twilio is configured. Ensure the following environment variables are set: SMS_MESSAGE_TEMPLATE, TWILIO_SID, TWILIO_MESSAGING_SID, TWILIO_AUTH_TOKEN.")

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
