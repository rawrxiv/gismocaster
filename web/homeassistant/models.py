from django.db import models

# Create your models here.


class Variable(models.Model):

    name = models.CharField(max_length=64)  # icon
    abbreviation = models.CharField(max_length=32)  # ic
    default_value = models.CharField(max_length=256, null=True, blank=True)  # mdi:light-switch

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )

    def __str__(self):
        return self.name


class Component(models.Model):

    name = models.CharField(max_length=32)  # Switch
    technical_name = models.CharField(max_length=32)  # switch
    variables = models.ManyToManyField(Variable)

    def __str__(self):
        return self.name


# python3 web/manage.py dumpdata homeassistant.variable --indent 4 > variable.json
