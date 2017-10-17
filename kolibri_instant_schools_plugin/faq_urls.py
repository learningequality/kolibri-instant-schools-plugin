from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.FAQView.as_view(), name='user'),
]
