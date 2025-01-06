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

router.register(r'phonesignup', PhoneNumberSignUpViewSet, basename='phonesignup')
router.register(r'passwordresettoken', PasswordResetTokenViewset, basename='passwordresettoken')
router.register(r'phoneaccountprofile', PhoneAccountProfileViewset, basename='phoneaccountprofile')
router.register(r'passwordchange', PasswordChangeViewset, basename='passwordchange')
router.register(r'facilityuserprofile', FacilityUserProfileViewset, basename='facilityuserprofile')
router.register(r'aboutfaq', AboutFAQViewSet, basename='aboutfaq')

urlpatterns = router.urls
