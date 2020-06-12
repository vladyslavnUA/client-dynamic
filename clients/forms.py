from django import forms
from django.forms import formset_factory

class ClientForm(forms.Form):
    name = forms.CharField(
        label='Client Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your clients\' full name'
        })
    )
    email = forms.CharField(
        label='Client Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your clients\' email'
        })
    )
    address = forms.CharField(
        label='Client Address',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your clients\' address'
        })
    )
# ClientFormset = formset_factory(ClientForm, extra=1)