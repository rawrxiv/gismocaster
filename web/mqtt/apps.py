from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MqttConfig(AppConfig):
    name = "mqtt"
    verbose_name = _("MQTT")

    def ready(self):
        # mqtt.init()
        from . import mqtt
        from . import signals

        mqtt.init()
