from __future__ import absolute_import, print_function, unicode_literals
from kolibri.core.webpack import hooks as webpack_hooks
from kolibri.plugins.base import KolibriPluginBase
from . import hooks, urls, about_urls


class User(KolibriPluginBase):
    def url_module(self):
        return urls

    def url_slug(self):
        return "^user/"


class UserAsset(webpack_hooks.WebpackBundleHook):
    unique_slug = "instant_schools_user_module"
    src_file = "assets/src/app.js"


class UserInclusionHook(hooks.UserSyncHook):
    bundle_class = UserAsset


class About(KolibriPluginBase):
    def url_module(self):
        return about_urls

    def url_slug(self):
        return "^about/"


class AboutAsset(webpack_hooks.WebpackBundleHook):
    unique_slug = "about_module"
    src_file = "assets/src/views/about/aboutApp.js"


class AboutInclusionHook(hooks.AboutSyncHook):
    bundle_class = AboutAsset
