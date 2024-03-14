from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={"class":"form-control"}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(max_length=25, widget= forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(max_length=25, widget= forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs= {"class":"form-control"}), label="Şifre")
    password2 = forms.CharField(widget = forms.PasswordInput(attrs= {"class":"form-control"}), label="Şifre Tekrar")



    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name","password1","password2")

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget= forms.TextInput(attrs={"class":"form-control"}))
    adress = forms.CharField(widget= forms.TextInput(attrs={"class":"form-control"}))
    city = forms.CharField(widget= forms.TextInput(attrs={"class":"form-control"}))
    country = forms.CharField(widget= forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = UserProfile
        fields = ['phone_number','adress','city','country']


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

        widgets = {
            'username': forms.TextInput(attrs={"class":"form-control"}),
            'email': forms.TextInput(attrs={"class":"form-control"}),
            'first_name': forms.TextInput(attrs={"class":"form-control"}),
            'last_name': forms.TextInput(attrs={"class":"form-control"}),

        }



