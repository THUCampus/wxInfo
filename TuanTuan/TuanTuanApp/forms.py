__author__ = 'Allen'

from django import forms
from django.db.models import get_model

from django.contrib import admin

from admin_uploads.widgets import WYMEditor, WYMEditorUpload

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


