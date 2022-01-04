from django.contrib import admin
from .models import Medicine, MedicineCompany


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'single_quantity', 'quantity', 'price', 'our_price', 'company','created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'single_quantity', 'quantity', 'price', 'our_price', 'company',)
    ordering = ('name', 'single_quantity', 'quantity', 'price', 'our_price', 'company',)
    filter_horizontal = ()


class MedicineCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', )
    ordering = ('name', )
    filter_horizontal = ()



admin.site.register(Medicine, MedicineAdmin)
admin.site.register(MedicineCompany, MedicineCompanyAdmin)