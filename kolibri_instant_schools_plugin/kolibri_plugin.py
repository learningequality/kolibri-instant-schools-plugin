from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import hooks
from os import getenv
from datetime import datetime
from kolibri.core.auth.constants.user_kinds import ANONYMOUS
from kolibri.core.hooks import NavigationHook
from kolibri.core.hooks import RoleBasedRedirectHook
from kolibri.core.webpack import hooks as webpack_hooks
from kolibri.plugins.base import KolibriPluginBase
from kolibri.core import theme_hook
from django.contrib.staticfiles.templatetags.staticfiles import static

APP_TITLE = getenv("INSTANT_SCHOOLS_APP_TITLE") or "Instant Schools"


class User(KolibriPluginBase):
    translated_view_urls = "urls"


class UserAsset(webpack_hooks.WebpackBundleHook):
    unique_slug = "instant_schools_user_module"
    src_file = "assets/src/app.js"


class UserInclusionHook(hooks.UserSyncHook):
    bundle_class = UserAsset


class LogInRedirect(RoleBasedRedirectHook):
    role = ANONYMOUS

    @property
    def url(self):
        return self.plugin_url(User, "user")


#  Navigation hooks
class LogInNavAction(NavigationHook, webpack_hooks.WebpackBundleHook):
    unique_slug = "instant_schools_user_module_login_nav_side_nav"
    src_file = "assets/src/views/SideNav/LoginSideNavEntry.vue"


class AboutNavAction(NavigationHook, webpack_hooks.WebpackBundleHook):
    unique_slug = "instant_schools_user_module_about_nav_side_nav"
    src_file = "assets/src/views/SideNav/AboutSideNavEntry.vue"


class ProfileNavAction(NavigationHook, webpack_hooks.WebpackBundleHook):
    unique_slug = "instant_schools_user_module_user_profile_nav_side_nav"
    src_file = "assets/src/views/SideNav/UserProfileSideNavEntry.vue"


class About(KolibriPluginBase):
    translated_view_urls = "about_urls"


class AboutAsset(webpack_hooks.WebpackBundleHook):
    unique_slug = "about_module"
    src_file = "assets/src/AboutApp.js"


class AboutInclusionHook(hooks.AboutSyncHook):
    bundle_class = AboutAsset


class InstantSchoolsThemeHook(theme_hook.ThemeHook):
    @property
    def theme(self):
        return {
            # metadata
            theme_hook.THEME_NAME: "Instant Schools Theme",
            theme_hook.THEME_VERSION: 1,  # increment when changes are made
            # specify primary and secondary brand colors
            theme_hook.BRAND_COLORS: {
                theme_hook.PRIMARY: {
                    theme_hook.COLOR_V50: "#fde7e6",
                    theme_hook.COLOR_V100: "#ffc7b8",
                    theme_hook.COLOR_V200: "#ffa18a",
                    theme_hook.COLOR_V300: "#ff7a5b",
                    theme_hook.COLOR_V400: "#ff5937",
                    theme_hook.COLOR_V500: "#ff3011",
                    theme_hook.COLOR_V600: "#fd290c",
                    theme_hook.COLOR_V700: "#ef2005",
                    theme_hook.COLOR_V800: "#e11300",
                    theme_hook.COLOR_V900: "#c90000",
                },
                theme_hook.SECONDARY: {
                    theme_hook.COLOR_V50: "#f7f7f7",
                    theme_hook.COLOR_V100: "#eeeeee",
                    theme_hook.COLOR_V200: "#e3e3e3",
                    theme_hook.COLOR_V300: "#d1d1d1",
                    theme_hook.COLOR_V400: "#acacac",
                    theme_hook.COLOR_V500: "#8b8b8b",
                    theme_hook.COLOR_V600: "#646464",
                    theme_hook.COLOR_V700: "#515151",
                    theme_hook.COLOR_V800: "#333333",
                    theme_hook.COLOR_V900: "#131313",
                },
            },
            theme_hook.TOKEN_MAPPING: {
                "primary": "#e11300",
                "appBar": "#333333",
            },
            # sign-in page config
            theme_hook.SIGN_IN: {
                theme_hook.BACKGROUND: static("instant-background.jpg"),
                theme_hook.SCRIM_OPACITY: 0,
                theme_hook.TITLE: APP_TITLE,
                theme_hook.TOP_LOGO: {
                    theme_hook.IMG_SRC: static("instant-school-logo.png"),
                    theme_hook.IMG_STYLE: "padding-left: 64px; padding-right: 64px; margin-bottom: 8px; margin-top: 8px",
                    theme_hook.IMG_ALT: None,
                },
                theme_hook.TITLE_STYLE: "font-style: NotoSans; color: #212121 !important",
                theme_hook.SHOW_POWERED_BY: False,
                theme_hook.SHOW_TITLE: True,
                theme_hook.SHOW_K_FOOTER_LOGO: False,
            },
            # side-nav config
            theme_hook.SIDE_NAV: {
                theme_hook.TITLE: APP_TITLE,
                theme_hook.BRANDED_FOOTER: {
                    theme_hook.LOGO: {
                        theme_hook.IMG_SRC: static("instant-school-logo.png"),
                    },
                    theme_hook.PARAGRAPH_ARRAY: [
                        APP_TITLE,
                        "\xa9 {} Vodafone Foundation".format(datetime.now().year),
                    ],
                },
                theme_hook.SHOW_K_FOOTER_LOGO: True,
            },
            # app bar config
            theme_hook.APP_BAR: {
                theme_hook.TOP_LOGO: {
                    theme_hook.IMG_SRC: static("instant-school-logo.png")
                }
            },
        }
