import os
from twilio.rest import Client
from django.core.urlresolvers import reverse

from ..auth.mapping import normalize_phone_number

SMS_MESSAGE_TEMPLATE = os.environ["SMS_MESSAGE_TEMPLATE"]
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]


def send_password_reset_link(prefix, phone, token, baseurl):

    phone = normalize_phone_number(phone)
    baseurl = baseurl.rstrip("/")
    endpointurl = reverse("kolibri:kolibri_instant_schools_plugin:instant_schools_auth")
    path = "{endpointurl}#/passwordreset/{phone}/{token}".format(endpointurl=endpointurl, token=token, phone=phone)


    url = "{baseurl}{path}".format(
        baseurl=baseurl, path=path
    )

    send_message(prefix, phone, SMS_MESSAGE_TEMPLATE.format(url=url))


def send_message(prefix, phone, message):

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
      messaging_service_sid='MG5789fbd6bb5607f3c1a10a020bb11ca3',
      to="{}{}".format(prefix, phone),
      body=message,
    )

    print(message.sid)
