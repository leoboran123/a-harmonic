from django.forms import ModelForm
from django.forms import ModelForm, TextInput, Textarea
from django import forms

from .models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ['first_name','last_name','adress','phone','city','country']
        widgets = {
            'first_name': TextInput(
                attrs={'type': "text", 'class': "form-control", 'id': "first_name", 'placeholder': "Your Name",
                       'required': "required",
                       'data-validation-required-message ': "Please enter your name"}),
            'last_name': TextInput(
                attrs={'type': 'text', 'class': "form-control", 'id': "last_name", 'placeholder': "Your Last Name",
                       'required': "required", 'data-validation-required-message': "Please enter your last name"}),
            'adress': TextInput(
                attrs={'type': "text", 'class': "form-control", 'id': "adress", 'placeholder': "Adress",
                       'required': "required", 'data-validation-required-message': "Please enter a adress"}),
            'phone': TextInput(
                attrs={'type': "text", 'class': "form-control", 'id': "phone", 'placeholder': "Phone",
                       'required': "required", 'data-validation-required-message': "Please enter a phone number"}),
            'city': TextInput(
                attrs={'type': "text", 'class': "form-control", 'id': "city", 'placeholder': "City",
                       'required': "required", 'data-validation-required-message': "Please enter a city"}),
            'country': TextInput(
                attrs={'type': "text", 'class': "form-control", 'id': "country", 'placeholder': "Country",
                       'required': "required", 'data-validation-required-message': "Please enter a country"})
        }
