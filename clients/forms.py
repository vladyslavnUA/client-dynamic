from django import forms
from django.forms import formset_factory
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'placeholder': '###-###-####'}),
        }