from django.conf.urls import url, include

from . import views
from .api_urls import urlpatterns

urlpatterns = [
    url(r'^api/', include(urlpatterns)),
    url(r'^$', views.UserView.as_view(), name='user'),
    url(r'^$', views.AboutView.as_view(), name='about'),
]
