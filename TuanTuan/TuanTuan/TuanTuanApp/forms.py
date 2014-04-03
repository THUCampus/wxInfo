__author__ = 'Allen'
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()