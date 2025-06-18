from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'id': 'username',
        'name':'username',
        'required': 'required'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'name':'password',
        'required': 'required'
    }))
