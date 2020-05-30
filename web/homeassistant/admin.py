from django.contrib import admin

# Register your models here.
from .models import Component, Variable

class ComponentAdmin(admin.ModelAdmin):
    model = Component
    list_display = ('name', 'technical_name')
    #m:m Variables

admin.site.register(Component)
admin.site.register(Variable)