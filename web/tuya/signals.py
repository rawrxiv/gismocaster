#https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
from .models import Setting, Device, Dps, Dpstype
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from . import mqtt


@receiver(post_save, sender=Device)
def save_device(sender, instance, **kwargs):
    # print(type(instance), instance.name)
    mqtt.publish_device(instance)


@receiver(pre_delete, sender=Device)
def delete_device(sender, instance, using, **kwargs):
    mqtt.unpublish_device(instance)


@receiver(post_save, sender=Dps)
def save_dps(sender, instance, **kwargs):
    mqtt.publish_devices() 


@receiver(pre_delete, sender=Dps)
def delete_dps(sender, instance, using, **kwargs):  
    mqtt.publish_devices() 


@receiver(post_save, sender=Dpstype)
def save_dps(sender, instance, **kwargs):   
    mqtt.publish_devices() 


@receiver(pre_delete, sender=Dpstype)
def delete_dps(sender, instance, using, **kwargs): 
    mqtt.publish_devices() 


@receiver(post_save, sender=Setting)
def save_setting(sender, instance, **kwargs):   
    mqtt.mqtt_connect()


@receiver(pre_delete, sender=Setting)
def delete_setting(sender, instance, using, **kwargs):  
    mqtt.mqtt_connect()