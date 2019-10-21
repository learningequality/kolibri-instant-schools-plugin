import requests
import smpplib2.gsm
import smpplib2.client
import smpplib2.consts
import smpplib2.exceptions
import urllib

from ..auth.mapping import normalize_phone_number

from .config import read_config


SOURCE_ADDR_TON = smpplib2.consts.SMPP_TON_INTL
SOURCE_ADDR_NPI = smpplib2.consts.SMPP_NPI_ISDN
DEST_ADDR_TON = smpplib2.consts.SMPP_TON_INTL
DEST_ADDR_NPI = smpplib2.consts.SMPP_NPI_ISDN


class SMSConnectionError(Exception):
    pass


def send_password_reset_link(phone, token, baseurl):

    conf = read_config()

    phone = normalize_phone_number(phone)
    baseurl = baseurl.rstrip("/")

    url = "{baseurl}/user/#/passwordreset/{phone}/{token}".format(baseurl=baseurl, token=token, phone=phone)

    send_message(phone, conf['SMS_MESSAGE_TEMPLATE'].format(url=url))


def send_message(phone, message):

    conf = read_config()

    # if a URL template has been specified, use the HTTP method of sending a message (e.g for Ghana)
    if conf["SMS_HTTP_URL_TEMPLATE"]:
        return send_message_by_http(phone, message, conf["SMS_HTTP_URL_TEMPLATE"])

    # encode the message into parts
    parts, encoding_flag, msg_type_flag = smpplib2.gsm.make_parts(message)

    # try connecting to the SMSC server
    try:
        client = smpplib2.client.Client(conf['SMSC_ADDRESS'], conf['SMSC_PORT'])
        client.connect()
    except smpplib2.exceptions.ConnectionError:
        raise SMSConnectionError("Unable to connect to SMSC server %s:%s (message was not sent)" % (conf['SMSC_ADDRESS'], conf['SMSC_PORT']))

    # log into the SMSC server
    client.bind_transceiver(system_id=conf['SMSC_SYSTEM_ID'], password=conf['SMSC_PASSWORD'], system_type='smpp')

    # loop over and send each of the message parts
    for part in parts:

        pdu = client.send_message(
            source_addr_ton=SOURCE_ADDR_TON,
            source_addr_npi=SOURCE_ADDR_NPI,
            source_addr=conf['SOURCE_ADDRESS'],

            dest_addr_ton=DEST_ADDR_TON,
            dest_addr_npi=DEST_ADDR_NPI,
            destination_addr=normalize_phone_number(phone),
            short_message=part,

            data_coding=encoding_flag,
            esm_class=msg_type_flag,
            registered_delivery=True,
        )


def send_message_by_http(phone, message, url_template):

    url = url_template.format(message=urllib.quote(message), phone=normalize_phone_number(phone))
    response = requests.get(url, timeout=20)

    print response.status_code, response.content

    if response.status_code != 200:
        raise SMSConnectionError("Error sending message via HTTP SMS server with address %s\n\t\tResponse: %s" % (url, response.content))
