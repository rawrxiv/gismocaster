from django.contrib import admin

from .models import Setting, Gismo, Dp, GismoModel, HAOverwrite

class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

class HAOverwriteInline(admin.TabularInline): 
    model = HAOverwrite

class DpAdmin(admin.ModelAdmin):
    inlines = [HAOverwriteInline, ]
    list_display = ('key', 'gismo_model', 'ha_component')


class GismoAdmin(admin.ModelAdmin):
    list_display = ('name', 'gismo_model', 'ip', 'ha_discovery', 'tuya_discovery')


class DpInline(admin.StackedInline): 
    model = Dp

class GismoModelAdmin(admin.ModelAdmin):
    inlines = [DpInline, ]
    list_display = ('name', 'protocol')


admin.site.register(Setting, SettingAdmin)
admin.site.register(Gismo, GismoAdmin)
admin.site.register(GismoModel, GismoModelAdmin)
# admin.site.register(HAOverwrite)
admin.site.register(Dp, DpAdmin)
