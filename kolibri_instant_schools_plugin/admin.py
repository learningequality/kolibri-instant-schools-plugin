from django.contrib import admin
from .models import AboutFAQ


class AboutFAQAdmin(admin.ModelAdmin):
    list_display = ('kind',)


admin.site.register(AboutFAQ, AboutFAQAdmin)
