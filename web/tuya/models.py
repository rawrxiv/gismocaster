from django.db import models
from homeassistant.models import Component, TopicValue

# Create your models here.
class Setting(models.Model):

    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Gismo(models.Model):

    name = models.CharField(max_length=32)
    gismo_model = models.ForeignKey(GismoModel, on_delete=models.CASCADE)

    deviceid = models.CharField(max_length=64, unique=True)
    localkey = models.CharField(max_length=64, unique=True)
    ip = models.GenericIPAddressField()

    ha_discovery = models.BooleanField()
    tuya_discovery = models.BooleanField()

    def __str__(self):
        return self.name


class Dp(models.Model):

    key = models.IntegerField()
    name = models.CharField(max_length=32)
    gismo_model = models.ForeignKey(GismoModel, on_delete=models.CASCADE)

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="bool", max_length=16
    )
    minimal = models.FloatField(
        default=0, help_text="for string length; for numerics min. value"
    )
    maximal = models.FloatField(
        default=255, help_text="for string length; for numerics max. value"
    )

    ha_component = models.ForeignKey(Component, on_delete=models.CASCADE)

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
