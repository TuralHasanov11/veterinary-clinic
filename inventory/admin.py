from django.contrib import admin
from .models import Equipment


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'total_price', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'quantity', 'price')
    ordering = ('name', 'quantity', 'price')
    filter_horizontal = ()



admin.site.register(Equipment, EquipmentAdmin)
