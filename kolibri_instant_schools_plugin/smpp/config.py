import ConfigParser
import logging
import os

from django.conf import settings

CONF_PATH = os.path.join(settings.KOLIBRI_HOME, "smpp.conf")

def write_default_config():

    config = ConfigParser.RawConfigParser()

    config.add_section('SMPP')
    config.set('SMPP', 'smsc_address', '127.0.0.1')
    config.set('SMPP', 'smsc_port', '1234')
    config.set('SMPP', 'smsc_system_id', 'pavel')
    config.set('SMPP', 'smsc_password', 'wpsd')
    config.set('SMPP', 'source_address', '11111111')
    config.set('SMPP', 'sms_message_template', 'Your Instant Schools password has been reset; the new temporary password is: %s')

    with open(CONF_PATH, 'wb') as configfile:
        config.write(configfile)

def read_config():

    if not os.path.isfile(CONF_PATH):
        write_default_config()

    config = ConfigParser.RawConfigParser()
    config.read(CONF_PATH)

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
        }

    except (ValueError, ConfigParser.NoOptionError) as e:

        raise Exception("There was an error trying to parse the SMS config at %s: %r" % (CONF_PATH, e))
