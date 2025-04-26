from django import forms
from .models import User
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'