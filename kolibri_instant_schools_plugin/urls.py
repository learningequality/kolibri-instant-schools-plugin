from django.conf.urls import include, url
from . import views
from .api_urls import urlpatterns

urlpatterns = [
    url('^api/', include(urlpatterns)),
    url(r'^', views.UserView.as_view(), name='user'),
]
