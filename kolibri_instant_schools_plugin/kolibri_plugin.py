from __future__ import absolute_import, print_function, unicode_literals
from kolibri.core.webpack import hooks as webpack_hooks
from kolibri.plugins.base import KolibriPluginBase
from . import hooks, urls, about_urls, faq_urls


class User(KolibriPluginBase):
    def url_module(self):
        return urls

    def url_slug(self):
        return "^user"


class UserAsset(webpack_hooks.WebpackBundleHook):
    unique_slug = "user_module"
    src_file = "assets/src/app.js"


class UserInclusionHook(hooks.UserSyncHook):
    bundle_class = UserAsset


class About(KolibriPluginBase):
    def url_module(self):
        return about_urls

    def url_slug(self):
        return "^about"


class FAQ(KolibriPluginBase):
    def url_module(self):
        return faq_urls

    def url_slug(self):
        return "^faq"
