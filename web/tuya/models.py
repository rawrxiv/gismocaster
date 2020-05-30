from django.db import models
from homeassistant.models import Component, Variable
# Create your models here.
class Setting(models.Model):

    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class GismoModel(models.Model):

    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, default="", null=True)
    image = models.URLField(default="", null=True)
    upload = models.FileField(default="", null=True)

    protocol_choices = [
        ('3.1', '3.1'),
        ('3.3', '3.3'),
    ]
    protocol = models.CharField(max_length=16, choices=protocol_choices, default='3.3')

    pref_cmd_choices = [
        (10, 'Dp Query'),
        (13, 'Control New'),
    ]
    pref_status_cmd = models.IntegerField(choices=pref_cmd_choices, default=10)

    def __str__(self):
        return self.name


class Gismo(models.Model):

    name = models.CharField(max_length=32)
    gismo_model = models.ForeignKey(GismoModel, on_delete=models.CASCADE)

    deviceid = models.CharField(max_length=64)
    localkey = models.CharField(max_length=64)
    ip = models.GenericIPAddressField()

    ha_discovery = models.BooleanField()
    tuya_discovery = models.BooleanField()

    def __str__(self):
        return self.name

class Dp(models.Model):

    key = models.IntegerField()    
    gismo_model = models.ForeignKey(GismoModel, on_delete=models.CASCADE)
    ha_component = models.ForeignKey(Component, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.key)} ({self.gismo_model.name} / {self.ha_component.name})"

class HAOverwrite(models.Model):

    dp = models.ForeignKey(Dp, on_delete=models.CASCADE)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.value
