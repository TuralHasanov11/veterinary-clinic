from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from .models import Equipment

class CreateOrUpdateEquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = ('name', 'quantity', 'price', 'note')





