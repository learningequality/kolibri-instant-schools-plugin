from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

from kolibri.auth.models import FacilityUser

from ...auth.hashing import get_hash_value, normalize_phone_number


class Command(BaseCommand):
    help = "Reset a user's password to a temporary value"

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('phonenumber', action='store',
            help='Phone number of user for whom we are resetting the password (no spaces).')

    def handle(self, *args, **options):
        
        phonenumber = normalize_phone_number(options['phonenumber'])
        username = get_hash_value(phonenumber)

        try:
            user = FacilityUser.objects.get(username=username)
        except FacilityUser.DoesNotExist:
            raise CommandError("User with phone number '%s' does not seem to exist." % phonenumber)

        new_password = get_random_string(length=8, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

        self.stdout.write("Resetting password for user with phone number '%s' to '%s'...\n" % (phonenumber, new_password))

        user.set_password(new_password)
        user.save()

        return "Password reset successfully!"
