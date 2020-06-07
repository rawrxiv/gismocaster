from django.contrib import admin

from .models import Gismo, GismoModel, Dp, HAOverwrite, DpName


class HAOverwriteInline(admin.TabularInline):
    model = HAOverwrite


class DpAdmin(admin.ModelAdmin):
    inlines = [
        HAOverwriteInline,
    ]
    list_display = ("key", "name", "ha_component")


class DpInline(admin.TabularInline):
    model = Dp


class DpNameInline(admin.TabularInline):
    model = DpName


class GismoAdmin(admin.ModelAdmin):
    list_display = ("name", "ip", "ha_discovery", "tuya_discovery")
    inlines = [
        DpNameInline,
    ]


class GismoModelAdmin(admin.ModelAdmin):
    inlines = [
        DpInline,
    ]
    list_display = ("name",)


admin.site.register(Gismo, GismoAdmin)
admin.site.register(GismoModel, GismoModelAdmin)
# admin.site.register(HAOverwrite)
admin.site.register(Dp, DpAdmin)
admin.site.register(DpName)
