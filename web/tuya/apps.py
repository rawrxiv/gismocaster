from django.apps import AppConfig
from . import mqtt
from django.utils.translation import ugettext_lazy as _

class TuyaConfig(AppConfig):
    name = 'tuya'
    verbose_name = _('tuya')

    def ready(self):
        mqtt.init()
        from . import signals
