from django.apps import AppConfig
from . import mqtt
from django.utils.translation import ugettext_lazy as _

class TuyamqttConfig(AppConfig):
    name = 'tuyamqtt'
    verbose_name = _('tuyamqtt')

    def ready(self):
        mqtt.init()
        from . import signals
