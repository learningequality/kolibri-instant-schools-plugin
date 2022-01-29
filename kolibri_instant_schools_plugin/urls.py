from django.conf.urls import url, include

from . import views
from .api_urls import urlpatterns

urlpatterns = [
    url(r'api/', include(urlpatterns)),
    url(r'auth/$', views.UserView.as_view(), name='instant_schools_auth'),
    url(r'about/$', views.AboutView.as_view(), name='instant_schools_about'),
]
