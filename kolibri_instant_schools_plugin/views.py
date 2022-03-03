from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from kolibri.core.decorators import cache_no_user_data
from kolibri.core.views import RootURLRedirectView


class UserView(TemplateView):
    template_name = "user/user.html"

    def get(self, request):
        if request.user.is_authenticated():
            return RootURLRedirectView.as_view()(request)
        return super(UserView, self).get(request)


class AboutView(TemplateView):
    template_name = "about/about.html"

