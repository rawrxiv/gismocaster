from django.db import models

from smart_selects.db_fields import ChainedForeignKey
from homeassistant.models import Component, TopicValue, Topic

# Create your models here.


class GismoModel(models.Model):

    name = models.CharField(max_length=32)

    protocol_choices = [
        ("3.1", "3.1"),
        ("3.3", "3.3"),
    ]
    protocol = models.CharField(max_length=16, choices=protocol_choices, default="3.3")

    pref_cmd_choices = [
        (10, "Dp Query"),
        (13, "Control New"),
    ]
    pref_status_cmd = models.IntegerField(choices=pref_cmd_choices, default=10)

    ha_component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Device type for Home Assistant",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Gismo(models.Model):

    name = models.CharField(
        max_length=32, unique=True, help_text="Common name for device."
    )
    gismo_model = models.ForeignKey(
        GismoModel, on_delete=models.CASCADE, help_text="Configuration for the device."
    )

    deviceid = models.CharField(max_length=64, unique=True)
    localkey = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(unique=True)

    ha_discovery = models.BooleanField(
        help_text="Send discovery messages to Home Assistant."
    )
    tuya_discovery = models.BooleanField(
        help_text="Send discovery messages to TuyaGateway."
    )

    def __str__(self):
        return self.name


class Dp(models.Model):

    key = models.IntegerField(help_text="The number of the data point.")
    name = models.CharField(max_length=32, help_text="Common name.")
    gismo_model = models.ForeignKey(GismoModel, on_delete=models.CASCADE)

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices,
        default="bool",
        max_length=16,
        help_text="Output type of the data point.",
    )
    minimal = models.FloatField(
        default=0, help_text="For string length; for numerics min. value."
    )
    maximal = models.FloatField(
        default=255, help_text="For string length; for numerics max. value."
    )

    ha_component = models.ForeignKey(
        Component, on_delete=models.CASCADE, help_text="Device type for Home Assistant"
    )
    # ha_topic = models.ForeignKey(
    #     Topic, on_delete=models.CASCADE, help_text="Publish topic for Home Assistant"
    # )

    # ha_component = ChainedForeignKey(
    #     GismoModel,
    #     chained_field="ha_component",
    #     chained_model_field="ha_component",
    #     show_all=False,
    #     auto_choose=True,
    #     sort=True)

    ha_topic = ChainedForeignKey(
        Topic,
        limit_choices_to={"topic_type": "publish"},
        chained_field="ha_component",
        chained_model_field="component",
        show_all=False,
        auto_choose=True,
        sort=True,
    )

    def __str__(self):
        return f"{str(self.key)} ({self.gismo_model.name} / {self.ha_component.name})"


class HAOverwrite(models.Model):

    dp = models.ForeignKey(Dp, on_delete=models.CASCADE)
    topic_value = models.ForeignKey(TopicValue, on_delete=models.CASCADE)
    value = models.CharField(max_length=256)

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]

    tuya_type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )

    tuya_value = models.CharField(max_length=256, null=True, blank=True,)

    def __str__(self):
        return self.value


class DpName(models.Model):

    gismo = models.ForeignKey(Gismo, on_delete=models.CASCADE)
    gismo_model = models.ForeignKey(GismoModel, on_delete=models.CASCADE)
    dp = models.ForeignKey(
        Dp, on_delete=models.CASCADE, help_text="Data point of the device."
    )
    name = models.CharField(max_length=32, help_text="Name for the dat point.")

    def __str__(self):
        return self.name
