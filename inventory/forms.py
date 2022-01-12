from django import forms
from .models import Equipment

class CreateOrUpdateEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ('name', 'quantity', 'price', 'note')





