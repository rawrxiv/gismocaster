from django.db import models

# Create your models here.


class Variable(models.Model):

    name = models.CharField(max_length=64)  # icon
    abbreviation = models.CharField(max_length=32)  # ic

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )
    default_value = models.CharField(
        max_length=256, null=True, blank=True
    )  # mdi:light-switch

    tuya_type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )

    tuya_value = models.CharField(max_length=256, null=True, blank=True,)

    def __str__(self):
        return self.name


class Topic(models.Model):

    name = models.CharField(max_length=64)  # icon
    abbreviation = models.CharField(max_length=32)  # ic
    specialized_for = models.CharField(max_length=64, null=True, blank=True)

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )
    default_value = models.CharField(
        max_length=256, null=True, blank=True
    )  # mdi:light-switch

    def __str__(self):
        if self.specialized_for:
            return f"{self.name} ({self.specialized_for})"
        return self.name


class TopicValue(models.Model):

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)  # icon
    abbreviation = models.CharField(max_length=32)  # ic

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )
    default_value = models.CharField(
        max_length=256, null=True, blank=True
    )  # mdi:light-switch

    tuya_type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )

    tuya_value = models.CharField(max_length=256, null=True, blank=True,)

    def __str__(self):
        return self.name


class Template(models.Model):

    name = models.CharField(max_length=64)  # icon
    abbreviation = models.CharField(max_length=32)  # ic

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )
    default_value = models.CharField(
        max_length=256, null=True, blank=True
    )  # mdi:light-switch

    def __str__(self):
        return self.name


class ComponentValue(models.Model):

    name = models.CharField(max_length=64)  # icon
    abbreviation = models.CharField(max_length=32)  # ic

    type_value_choices = [
        ("string", "String"),
        ("int", "Integer"),
        ("bool", "Boolean"),
        ("float", "Float"),
    ]
    type_value = models.CharField(
        choices=type_value_choices, default="string", max_length=16
    )
    default_value = models.CharField(
        max_length=256, null=True, blank=True
    )  # mdi:light-switch

    def __str__(self):
        return self.name


class Component(models.Model):

    name = models.CharField(max_length=32)  # Switch
    technical_name = models.CharField(max_length=32)  # switch
    values = models.ManyToManyField(ComponentValue)
    topics = models.ManyToManyField(Topic)
    templates = models.ManyToManyField(Template)

    def __str__(self):
        return self.name


# python3 web/manage.py dumpdata homeassistant.variable --indent 4 > variable.json
