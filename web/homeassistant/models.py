from django.db import models

# Create your models here.

class Variable(models.Model):

    name = models.CharField(max_length=64) #icon
    abbreviation = models.CharField(max_length=32) #ic
    default_value = models.CharField(max_length=256) #mdi:light-switch

    def __str__(self):
        return self.name

class Component(models.Model):

    name = models.CharField(max_length=32)  #Switch
    technical_name = models.CharField(max_length=32) #switch
    variables = models.ManyToManyField(Variable)

    def __str__(self):
        return self.name
