# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
from .models import Setting, Gismo, Dp, GismoModel, HAOverwrite
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from . import mqtt


@receiver(post_save, sender=Gismo)
def save_gismo(sender, instance, **kwargs):
    # print(type(instance), instance.name)
    # mqtt.publish_gismo(instance)
    pass


@receiver(pre_delete, sender=Gismo)
def delete_gismo(sender, instance, using, **kwargs):
    mqtt.unpublish_gismo(instance)


@receiver(post_save, sender=Dp)
def save_dps(sender, instance, **kwargs):
    # mqtt.publish_gismos()
    pass


@receiver(pre_delete, sender=Dp)
def delete_dps(sender, instance, using, **kwargs):
    mqtt.publish_gismos()


# @receiver(post_save, sender=Dpstype)
# def save_dps(sender, instance, **kwargs):
#     mqtt.publish_gismos()


# @receiver(pre_delete, sender=Dpstype)
# def delete_dps(sender, instance, using, **kwargs):
#     mqtt.publish_gismos()


@receiver(post_save, sender=Setting)
def save_setting(sender, instance, **kwargs):
    mqtt.mqtt_connect()


@receiver(pre_delete, sender=Setting)
def delete_setting(sender, instance, using, **kwargs):
    mqtt.mqtt_connect()
