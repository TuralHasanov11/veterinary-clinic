from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import Animal, MedicalExamination, Doctor, Feed
from datetime import date

class CreateAnimalForm(forms.ModelForm):
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Sahibi'}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ləqəb'}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0}))
    weight = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control','step':'0.01', 'min':0}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'xx xxx xx xx'}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'25', 'placeholder':'Əlavə məlumat'}))
    doctor = forms.ModelChoiceField(queryset= Doctor.objects.all(), empty_label="Həkimi seçin", widget=forms.Select(attrs={'class':'form-select'}))
    examination = forms.ModelChoiceField(queryset= MedicalExamination.objects.all(), empty_label="Müayinəni seçin", widget=forms.Select(attrs={'class':'form-select'}))
    breed = forms.ChoiceField(choices=Animal.BREEDS, widget=forms.Select(attrs={'class':'form-select'}))
    color = forms.ChoiceField(choices=Animal.COLORS, widget=forms.Select(attrs={'class':'form-select'}))
    entry_date = forms.DateTimeField(required=False, widget = forms.TextInput(attrs={'class':'form-control', }), initial=date.today())
    price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Animal
        fields = ['name', 'owner', 'breed', 'age', 'weight','color', 'entry_date','phone','note', 'examination','doctor']

class UpdateAnimalForm(forms.ModelForm):
    owner = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Sahibi'}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ləqəb'}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0}))
    weight = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control','step':'0.01', 'min':0}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'xx xxx xx xx'}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'25', 'placeholder':'Əlavə məlumat'}))
    doctor = forms.ModelChoiceField(queryset= Doctor.objects.all(), empty_label="Həkimi seçin", widget=forms.Select(attrs={'class':'form-select'}))
    examination = forms.ModelChoiceField(queryset= MedicalExamination.objects.all(), empty_label="Müayinəni seçin", widget=forms.Select(attrs={'class':'form-select'}))
    breed = forms.ChoiceField(choices=Animal.BREEDS, widget=forms.Select(attrs={'class':'form-select'}))
    color = forms.ChoiceField(choices=Animal.COLORS, widget=forms.Select(attrs={'class':'form-select'}))
    entry_date = forms.DateTimeField(required=False, widget = forms.TextInput(attrs={'class':'form-control', }))
    price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Animal
        fields = ['name', 'owner', 'breed', 'age', 'weight','color', 'entry_date','phone','note', 'examination','doctor']


