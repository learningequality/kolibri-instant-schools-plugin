import logging
import os

from django.conf import settings
from kolibri.utils import conf

CONF_PATH = os.path.join(conf.KOLIBRI_HOME, "smpp.conf")

#py2/py3 compatibility
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

def write_default_config():

    config = ConfigParser.RawConfigParser()

    config.add_section('SMPP')
    config.set('SMPP', 'smsc_address', '127.0.0.1')
    config.set('SMPP', 'smsc_port', '2775')
    config.set('SMPP', 'smsc_system_id', 'smppclient1')
    config.set('SMPP', 'smsc_password', 'password')
    config.set('SMPP', 'source_address', '11111111')
    config.set('SMPP', 'sms_message_template', 'To reset your Instant Schools account password, please click the following link: {url}')
    config.set('SMPP', 'sms_http_url_template', '')

    with open(CONF_PATH, 'wb') as configfile:
        config.write(configfile)

def read_config():

    if not os.path.isfile(CONF_PATH):
        write_default_config()

    config = ConfigParser.RawConfigParser()
    config.read(CONF_PATH)

    try:
        sms_http_url_template = config.get('SMPP', 'sms_http_url_template'),
        if sms_http_url_template and isinstance(sms_http_url_template, tuple):
            sms_http_url_template = sms_http_url_template[0]
        if sms_http_url_template:
            if "{phone}" not in sms_http_url_template or "{message}" not in sms_http_url_template:
                raise Exception("In the SMS config (%s) sms_http_url_template must contain both {{message}} and {{phone}}" % (CONF_PATH))
    except (ValueError, ConfigParser.NoOptionError):
        sms_http_url_template = ""

    try:

        if config.get('SMPP', 'SMSC_ADDRESS') == '127.0.0.1':
            logging.warn("You must update the SMPP config at %s in order to send SMS messages." % CONF_PATH)

        return {
            'SMSC_ADDRESS': config.get('SMPP', 'smsc_address'),
            'SMSC_PORT': config.getint('SMPP', 'smsc_port'),
            'SMSC_SYSTEM_ID': config.get('SMPP', 'smsc_system_id'),
            'SMSC_PASSWORD': config.get('SMPP', 'smsc_password'),
            'SOURCE_ADDRESS': config.get('SMPP', 'source_address'),
            'SMS_MESSAGE_TEMPLATE': config.get('SMPP', 'sms_message_template'),
            'SMS_HTTP_URL_TEMPLATE': sms_http_url_template,
        }

    except (ValueError, ConfigParser.NoOptionError) as e:

        raise Exception("There was an error trying to parse the SMS config at %s: %r" % (CONF_PATH, e))
