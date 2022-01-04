from django.contrib import admin
from .models import Doctor, Feed, Animal, MedicalExamination
from .forms import CreateAnimalForm, UpdateAnimalForm


class AnimalAdmin(admin.ModelAdmin):

    form = UpdateAnimalForm
    add_form = CreateAnimalForm

    list_display = ('name', 'owner', 'breed_name', 'age', 'weight', 'color_name', 'entry_date', 'phone', 'examination','doctor','created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'owner', 'breed', 'age', 'weight', 'color', 'entry_date', 'phone', 'examination','doctor')
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name','owner','breed', 'entry_date', 'phone')
    ordering = ('name','owner','breed', 'entry_date', 'phone')
    filter_horizontal = ()


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ()


class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'weight', 'total_weight', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'quantity', 'weight', 'total_weight')
    ordering = ('name', 'quantity', 'weight')
    filter_horizontal = ()


class MedicalExaminationAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_price', 'max_price', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'min_price', 'max_price')
    ordering = ('name', 'min_price', 'max_price')
    filter_horizontal = ()



admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(MedicalExamination, MedicalExaminationAdmin)