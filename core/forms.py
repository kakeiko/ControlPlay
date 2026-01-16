from django import forms
from .models import Profile, Device, Rule, UsageSession

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nome', 'dono']
        widgets = {
            'nome':forms.TextInput({'class': 'input-nome', 'placeholder': 'nome do perfil'})
        }

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['nome', 'macAddress']
        widgets = {
            'nome':forms.TextInput({'class': 'input-nome', 'placeholder': 'nome do perfil'}),
        }

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['tempo']
        widgets = {
            'tempo': forms.NumberInput({'class': 'input-tempo', 'placeholder': 'Tempo em minutos'})
        }

class UsageSessionForm(forms.ModelForm):
    class Meta:
        model = UsageSession
        fields = ['device', 'usuario']