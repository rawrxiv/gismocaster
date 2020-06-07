from django.contrib import admin

# Register your models here.
from .models import Component, Template, Topic, TopicValue, ComponentValue


class TopicValueInline(admin.TabularInline):
    model = TopicValue


class TopicAdmin(admin.ModelAdmin):
    model = Topic
    inlines = [
        TopicValueInline,
    ]
    list_display = ("name", "abbreviation")


class ComponentAdmin(admin.ModelAdmin):
    model = Component
    list_display = ("name", "technical_name")


admin.site.register(Component, ComponentAdmin)
admin.site.register(Template)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicValue)
admin.site.register(ComponentValue)
