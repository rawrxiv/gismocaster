from django.contrib import admin
from django import forms

from .models import Gismo, GismoModel, Dp, HAOverwrite, DpName
from homeassistant.models import Component, TopicValue, Topic


class HAOverwriteInline(admin.TabularInline):
    model = HAOverwrite


class SupplierAdminForm(forms.ModelForm):
    class Meta:
        model = Dp
        fields = "__all__"  # for Django 1.8+

    def __init__(self, *args, **kwargs):
        super(SupplierAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            print(self.instance.gismo_model_id)
            gismo_model = list(
                GismoModel.objects.filter(id=self.instance.gismo_model_id).values()
            )
            if len(gismo_model) > 0:
                print(gismo_model[0])
                self.fields["ha_component"].queryset = Component.objects.filter(
                    id=gismo_model[0]["ha_component_id"]
                )


class DpAdmin(admin.ModelAdmin):

    inlines = [
        HAOverwriteInline,
    ]
    list_display = ("key", "name", "ha_component")


class DpInline(admin.TabularInline):
    form = SupplierAdminForm
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


"""
class SupplierAdminForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__" # for Django 1.8+


    def __init__(self, *args, **kwargs):
        super(SupplierAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['cat'].queryset = Cat.objects.filter(supplier=self.instance)

class SupplierAdmin(admin.ModelAdmin):
    form = SupplierAdminForm
"""
