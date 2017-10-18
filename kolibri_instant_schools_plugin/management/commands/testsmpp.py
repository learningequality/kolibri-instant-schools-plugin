from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from kolibri.auth.models import FacilityUser

from ...auth.mapping import normalize_phone_number

from ...smpp.utils import send_message


class Command(BaseCommand):
    help = "Send a test message via SMS to test out the SMPP settings."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('phonenumber', action='store',
            help='Phone number to which to send a test SMS')

    def handle(self, *args, **options):
        
        phonenumber = normalize_phone_number(options['phonenumber'])

        send_message(phonenumber, "This is a test! %s" % timezone.now())

        self.stdout.write("SMS sent successfully!")
