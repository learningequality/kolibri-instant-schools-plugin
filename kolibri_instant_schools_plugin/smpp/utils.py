import smpplib2.gsm
import smpplib2.client
import smpplib2.consts
import smpplib2.exceptions

from ..auth.mapping import normalize_phone_number

from .config import read_config


SOURCE_ADDR_TON = smpplib2.consts.SMPP_TON_INTL
SOURCE_ADDR_NPI = smpplib2.consts.SMPP_NPI_ISDN
DEST_ADDR_TON = smpplib2.consts.SMPP_TON_INTL
DEST_ADDR_NPI = smpplib2.consts.SMPP_NPI_ISDN


class SMPPConnectionError(Exception):
    pass


def send_password_reset_link(phone, token, baseurl):
    
    conf = read_config()

    phone = normalize_phone_number(phone)
    baseurl = baseurl.rstrip("/")

    url = "{baseurl}/user/#/passwordreset/{phone}/{token}".format(baseurl=baseurl, token=token, phone=phone)
    
    send_message(phone, conf['SMS_MESSAGE_TEMPLATE'].format(url=url))


def send_message(phone, message):

    conf = read_config()

    # encode the message into parts
    parts, encoding_flag, msg_type_flag = smpplib2.gsm.make_parts(message)

    # try connecting to the SMSC server
    try:
        client = smpplib2.client.Client(conf['SMSC_ADDRESS'], conf['SMSC_PORT'])
        client.connect()
    except smpplib2.exceptions.ConnectionError:
        raise SMPPConnectionError("Unable to connect to SMSC server %s:%s (message was not sent)" % (conf['SMSC_ADDRESS'], conf['SMSC_PORT']))

    # log into the SMSC server
    client.bind_transceiver(system_id=conf['SMSC_SYSTEM_ID'], password=conf['SMSC_PASSWORD'])

    # loop over and send each of the message parts
    for part in parts:

        pdu = client.send_message(
            source_addr_ton=SOURCE_ADDR_TON,
            source_addr_npi=SOURCE_ADDR_NPI,
            source_addr=conf['SOURCE_ADDRESS'], 

            dest_addr_ton=DEST_ADDR_TON,
            dest_addr_npi=DEST_ADDR_NPI,
            destination_addr=phone,
            short_message=part,

            data_coding=encoding_flag,
            esm_class=msg_type_flag,
            registered_delivery=True,
        )
