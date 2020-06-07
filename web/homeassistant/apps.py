from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HomeassistantConfig(AppConfig):
    name = "homeassistant"
    verbose_name = _("Home Assistant")
