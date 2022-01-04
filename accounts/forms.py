from django import forms
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import fields
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Account

class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(max_length=60, help_text='Email is required and should be valid email address')
    # phone_number = forms.RegexField(regex=r'^\+994[1-9]{1}[0-9]{3,14}$', help_text = ("Phone number must be entered in the format: '+994 xx xxx xx xx'"))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Adı'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Soyadı'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'İstifadəçi adı'}))
    is_admin = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   
    class Meta:
        model = Account
        # fields = ('first_name','last_name','email', 'username', 'is_admin','password1', 'password2')
        fields = ('first_name','last_name', 'is_admin', 'username', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Şifrə'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'İstifadəçi adı'}))
    
    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):

        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']

            if not authenticate(username=username, password=password):
                raise forms.ValidationError('İstifadəçi adı yaxud şifrə yalnışdır!')


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Adı'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Soyadı'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'İstifadəçi adı'}))
    is_admin = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    new_password2 = forms.CharField(label='New Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Account
        fields= ('username','first_name','last_name','is_admin',)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                profile = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(f'Username {profile} does not exist')

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password", "")
        if old_password and self.instance.check_password(old_password):
            raise ValidationError("old Passwords don't match")
        return True

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1",'')
        new_password2 = self.cleaned_data.get("new_password2",'')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("new Passwords don't match")
        return True

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("new_password1",''):
            user.set_password(self.cleaned_data.get("new_password1"))
        if commit:
            user.save()
        return user
