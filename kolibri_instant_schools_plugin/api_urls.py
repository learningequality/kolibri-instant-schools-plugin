from rest_framework import routers

from .auth.api import PhoneNumberSignUpViewSet, PasswordResetTokenViewset, PhoneAccountProfileViewset, PasswordChangeViewset

router = routers.SimpleRouter()

router.register(r'phonesignup', PhoneNumberSignUpViewSet, base_name='phonesignup')
router.register(r'passwordresettoken', PasswordResetTokenViewset, base_name='passwordresettoken')
router.register(r'phoneaccountprofile', PhoneAccountProfileViewset, base_name='phoneaccountprofile')
router.register(r'passwordchange', PasswordChangeViewset, base_name='passwordchange')

urlpatterns = router.urls
