from django import forms
from .models import Problem, UserAction
from django.contrib.auth.models import User


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description']


class UserActionForm(forms.ModelForm):
    class Meta:
        model = UserAction
        fields = ['action']
