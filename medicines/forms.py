from django import forms
from django.forms import fields
from .models import Medicine, MedicineCompany

class CreateMedicineForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset= MedicineCompany.objects.all(), empty_label="Şirkəti seçin")
    class Meta:
        model = Medicine
        fields = ['name', 'price', 'quantity', 'our_price', 'company']

class UpdateMedicineForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset= MedicineCompany.objects.all())
    class Meta:
        model=Medicine
        fields = ['name', 'price', 'quantity', 'our_price', 'company']


class CreateMedicineCompanyForm(forms.ModelForm):

    class Meta:
        model = MedicineCompany
        fields = ['name']

class UpdateMedicineCompanyForm(forms.ModelForm):
    class Meta:
        model=Medicine
        fields = ['name']
