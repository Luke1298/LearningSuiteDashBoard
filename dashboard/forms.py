from django import forms
import utils

class SignInForm(forms.Form):
    netid = forms.CharField(label='Your netid', max_length=100)
    password = forms.CharField(label='Your password', max_length=100)
