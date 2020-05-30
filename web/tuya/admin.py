from django.contrib import admin

from .models import Setting, Gismo, Dp, HAOverwrite


class SettingAdmin(admin.ModelAdmin):
    list_display = ("name", "value")


class HAOverwriteInline(admin.TabularInline):
    model = HAOverwrite


class DpAdmin(admin.ModelAdmin):
    inlines = [
        HAOverwriteInline,
    ]
    list_display = ("key", "name", "ha_component")

class DpInline(admin.StackedInline):
    model = Dp

class GismoAdmin(admin.ModelAdmin):
    list_display = ("name", "ip", "protocol", "ha_discovery", "tuya_discovery")
    inlines = [
        DpInline,
    ]

# class GismoModelAdmin(admin.ModelAdmin):GismoModel,
#     inlines = [
#         DpInline,
#     ]
#     list_display = ("name")


admin.site.register(Setting, SettingAdmin)
admin.site.register(Gismo, GismoAdmin)
# admin.site.register(GismoModel, GismoModelAdmin)
# admin.site.register(HAOverwrite)
admin.site.register(Dp, DpAdmin)
