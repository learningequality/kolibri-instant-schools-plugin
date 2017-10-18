from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from rest_framework import filters, permissions, status, viewsets, serializers
from rest_framework.response import Response
from kolibri.auth.models import Facility, FacilityUser
from kolibri.auth.api import SignUpViewSet

from .mapping import get_usernames, create_new_username
from ..models import PasswordResetToken, PhoneToUsernameMapping
from ..smpp.utils import send_password_reset_link, SMPPConnectionError

from kolibri.auth.serializers import FacilityUserSerializer


class PhoneNumberSignupFacilityUserSerializer(FacilityUserSerializer):

    def validate_username(self, value):
        if FacilityUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(_('An account already exists for this phone number. To add a new profile ' +
                                                'under this account, you must first login. If you have forgotten your ' +
                                                'password, you can reset it using the link on the login page.'))
        return value


class PhoneNumberSignUpViewSet(SignUpViewSet):

    serializer_class = PhoneNumberSignupFacilityUserSerializer

    def extract_request_data(self, request):
        data = super(PhoneNumberSignUpViewSet, self).extract_request_data(request)

        # if there are already users for this number, use one, to trigger a validation error, else create a new one
        usernames = get_usernames(data["username"])
        if usernames:
            data["username"] = usernames[0]
        else:
            data["username"] = create_new_username(data["username"])

        return data


class PasswordResetTokenViewset(viewsets.ViewSet):

    def create(self, request):
        """
        Initiate the password reset process by generating a token for a phone number, and sending a link via SMS.

        Usage:

            POST {"phone": "<phone>"} to /user/api/passwordresettoken/
                If it succeeds, it returns status 201.
                If the phone doesn't have an account, it returns status 400, and body is a translated error message.
                If the SMS fails to send, it returns status 500, and the body is a translated error message.
        """

        # extract the phone number from the request
        phone = request.data.get('phone', '')

        # ensure we have an account for this phone number
        if not get_usernames(phone):
            return Response(_("No account found for this phone number."), status=status.HTTP_400_BAD_REQUEST)

        # generate a new token for the phone number
        token = PasswordResetToken.generate_new_token(phone=phone)

        # determine base URL from the scheme/host in this request, so we send people back to a server they can access
        baseurl = "{scheme}://{host}".format(scheme=request.scheme, host=request.META['HTTP_HOST'])

        # send the password reset URL to the phone number via SMS
        try:
            send_password_reset_link(phone, token.token, baseurl)
        except SMPPConnectionError:
            return Response(_("Error sending SMS message; please try again later."),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return a 201 to indicate having successfully sent the reset URL
        return Response("", status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Check validity of token (from the /user/#/passwordreset/<phone>/<token> page).

        Usage:

            GET `/user/api/passwordresettoken/<token>/?phone=<phone>`
                If token exists and is valid, returns status 200.
                Otherwise, returns status 400.
        """
        phone = request.query_params.get('phone', '')

        try:
            obj = PasswordResetToken.objects.get(token=pk, phone=phone)
        except PasswordResetToken.DoesNotExist:
            obj = None
        if obj and obj.is_valid():
            return Response("OK", status=status.HTTP_200_OK)
        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeViewset(viewsets.ViewSet):

    def create(self, request):
        """
        Change the password for the full set of FacilityUser profiles associated with a phone number.

        Usage:

            If the user is not logged in (i.e. from password reset page linked from SMS), send:
                POST {"password": "<password>", "phone": "<phone>", "token": "<token>"} to /user/api/passwordchange/

            If the user is logged in (i.e. for password change form on profile page), send:
                POST {"password": "<password>"} to /user/api/passwordchange/

                    If it succeeds, it returns status 200.
                    If user is not logged in (or doesn't match phone) and no valid token provided, returns status 401.
        """

        resettoken = None

        # extract the token from the request data
        token = request.data.get('token', '')

        if token:
            # try to find a reset token matching the phone number and token, otherwise error out
            phone=request.data.get('phone', '')
            try:
                resettoken = PasswordResetToken.objects.get(phone=phone, token=token)
            except PasswordResetToken.DoesNotExist:
                return Response("", status=status.HTTP_401_UNAUTHORIZED)
        else:
            # use the phone number associated with the logged in user
            try:
                phone = PhoneToUsernameMapping.objects.get(username=getattr(request.user, "username")).phone
            except PhoneToUsernameMapping.DoesNotExist:
                return Response("", status=status.HTTP_401_UNAUTHORIZED)

        # extract the password from the request data
        password = request.data.get('password', '')

        # get the full list of usernames associated with this account
        usernames = get_usernames(phone)

        # update the password for each of the accounts
        with transaction.atomic():
            for user in FacilityUser.objects.filter(username__in=usernames):
                user.set_password(password)
                user.save()
            # mark the token as having been used
            if resettoken:
                resettoken.use_token()

        # return a 200 to indicate having successfully changed the passwords
        return Response("", status=status.HTTP_200_OK)


class PhoneAccountProfileViewset(viewsets.ViewSet):

    def create(self, request):
        """
        Create a new "profile" (FacilityUser) for a given phone number.

        Usage:

            POST {"phone": "<phone>", "password": "<password>", "full_name": "<full_name>"} to /user/api/phoneaccountprofile/
                If it succeeds, it returns status 201 with the new username in the body.
                If it fails, it returns status 401.
        """

        # extract the data from the request
        phone = request.data['phone']
        password = request.data['password']
        full_name = request.data['full_name']

        # get the list of existing profiles (users) for the phone number
        users = FacilityUser.objects.filter(username__in=get_usernames(phone))
        if not users:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)

        # verify that the password provided matches the existing password associated with the phone number
        if not users[0].check_password(password):
            return Response("", status=status.HTTP_401_UNAUTHORIZED)

        # generate a new username for this phone number
        username = create_new_username(phone)

        # create the new FacilityUser for the profile
        user = FacilityUser(username=username, full_name=full_name, facility=users[0].facility)
        user.set_password(password)
        user.save()

        return Response(username, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        Get a list of profiles associated with a phone number (authenticated by password).

        Usage:

            GET /user/api/phoneaccountprofile/?phone=<phone>&password=<password>
                If successful, returns status 200 with a list of dicts with `full_name` and `username`.
                If no accounts are found, returns status 404.
                If password fails, returns status 401.
        """
        # extract the phone and password from the query params
        phone = request.query_params.get('phone', '')
        password = request.query_params.get('password', '')

        # get all user profiles associated with the phone number
        users = FacilityUser.objects.filter(username__in=get_usernames(phone))

        # return a 404 if there are no users for this phone number
        if not users:
            return Response("", status=status.HTTP_404_NOT_FOUND)

        # verify that the password provided matches the existing password associated with the phone number
        if not users[0].check_password(password):
            return Response("", status=status.HTTP_401_UNAUTHORIZED)

        return Response([{"username": user.username, "full_name": user.full_name} for user in users], status=status.HTTP_200_OK)
