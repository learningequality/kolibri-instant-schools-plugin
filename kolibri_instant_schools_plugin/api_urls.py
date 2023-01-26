from rest_framework import routers

from .auth.api import (
    PhoneNumberSignUpViewSet,
    PasswordResetTokenViewset,
    PhoneAccountProfileViewset,
    PasswordChangeViewset,
    FacilityUserProfileViewset,
    AboutFAQViewSet
)

router = routers.SimpleRouter()

router.register(r'phonesignup', PhoneNumberSignUpViewSet, base_name='phonesignup')
router.register(r'passwordresettoken', PasswordResetTokenViewset, base_name='passwordresettoken')
router.register(r'phoneaccountprofile', PhoneAccountProfileViewset, base_name='phoneaccountprofile')
router.register(r'passwordchange', PasswordChangeViewset, base_name='passwordchange')
router.register(r'facilityuserprofile', FacilityUserProfileViewset, base_name='facilityuserprofile')
router.register(r'aboutfaq', AboutFAQViewSet, base_name='aboutfaq')

urlpatterns = router.urls
