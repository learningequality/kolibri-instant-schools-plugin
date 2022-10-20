from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from os import getenv
from datetime import datetime
from kolibri.core.auth.constants.user_kinds import ANONYMOUS
from kolibri.core.hooks import NavigationHook
from kolibri.core.hooks import RoleBasedRedirectHook
from kolibri.core.webpack import hooks as webpack_hooks
from kolibri.plugins import KolibriPluginBase
from kolibri.plugins.hooks import register_hook
from kolibri.core import theme_hook
from django.contrib.staticfiles.templatetags.staticfiles import static

APP_TITLE = getenv("INSTANT_SCHOOLS_APP_TITLE") or "Instant Schools"


class User(KolibriPluginBase):
    translated_view_urls = "urls"
    untranslated_view_urls = "untranslated_urls"

    @property
    def url_slug(self):
        return 'user'


@register_hook
class UserAsset(webpack_hooks.WebpackBundleHook):
    bundle_id = "instant_schools_auth"

    @property
    def plugin_data(self):
        return {
            "COUNTRY_CODE": getenv("COUNTRY_CODE") or None,
        }


@register_hook
class AboutAsset(webpack_hooks.WebpackBundleHook):
    bundle_id="instant_schools_about"

@register_hook
class LogInRedirect(RoleBasedRedirectHook):
    @property
    def roles(self):
        return (ANONYMOUS,)

    @property
    def url(self):
        return self.plugin_url(User, "instant_schools_auth")


#  Navigation hooks
@register_hook
class LogInNavAction(NavigationHook, webpack_hooks.WebpackBundleHook):
    bundle_id="instant_schools_login_nav_action"


@register_hook
class AboutNavAction(NavigationHook, webpack_hooks.WebpackBundleHook):
    bundle_id="instant_schools_about_nav_action"


@register_hook
class DefaultThemeHook(theme_hook.ThemeHook):
    @property
    def theme(self):

        logo_file = static("instant-school-logo.png")

        return {
            # specify primary and secondary brand colors
            "brandColors": {
                "primary": {
                    "v_50": "#fde7e6",
                    "v_100": "#ffc7b8",
                    "v_200": "#ffa18a",
                    "v_300": "#ff7a5b",
                    "v_400": "#ff5937",
                    "v_500": "#ff3011",
                    "v_600": "#fd290c",
                    "v_700": "#ef2005",
                    "v_800": "#e11300",
                    "v_900": "#c90000",
                },
                "secondary": {
                    "v_50": "#f7f7f7",
                    "v_100": "#eeeeee",
                    "v_200": "#e3e3e3",
                    "v_300": "#d1d1d1",
                    "v_400": "#acacac",
                    "v_500": "#8b8b8b",
                    "v_600": "#646464",
                    "v_700": "#515151",
                    "v_800": "#333333",
                    "v_900": "#131313",
                },
            },
            "tokenMapping": {
                "primary": "#e11300",
                "appBar": "#333333",
            },
            # sign-in page config
            "signIn": {
                "background": static("instant-background.jpg"),
                "scrimOpacity": 0,
                "title": APP_TITLE,
                "topLogo": {
                    "src": logo_file,
                    "style": "padding-left: 64px; padding-right: 64px; margin-bottom: 8px; margin-top: 8px",
                    "alt": None,
                },
                "titleStyle": "font-style: NotoSans; color: #212121 !important",
                "showPoweredBy": False,
                "showTitle": True,
                "showKolibriFooterLogo": False,
            },
            # side-nav config
            "sideNav": {
                "title": APP_TITLE,
                "brandedFooter": {
                    "logo": {
                        "src": logo_file,
                    },
                    "paragraphArray": [
                        APP_TITLE,
                        "\xa9 {} Vodafone Foundation".format(datetime.now().year),
                    ],
                },
                "showKolibriFooterLogo": True,
            },
            # app bar config
            "appBar": {
                "topLogo": {
                    "src": logo_file,
                },
            },
        }
