from django.contrib import admin

# Register your models here.
from .models import Component, Template, Topic, TopicValue, ComponentValue


class ComponentAdmin(admin.ModelAdmin):
    model = Component
    list_display = ("name", "technical_name")
    # m:m Variables


admin.site.register(Component)
admin.site.register(Template)
admin.site.register(Topic)
admin.site.register(TopicValue)
admin.site.register(ComponentValue)
