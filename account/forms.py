from django import forms
from django.contrib.auth.models import User
from .models import *
# Create your models here.

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite tu contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']
            
            
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
    
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']