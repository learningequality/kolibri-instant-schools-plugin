from rest_framework import routers

from .auth.api import PhoneNumberSignUpViewSet

router = routers.SimpleRouter()

router.register(r'phonesignup', PhoneNumberSignUpViewSet, base_name='phonesignup')

urlpatterns = router.urls
