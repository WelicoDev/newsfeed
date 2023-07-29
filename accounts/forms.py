from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password" , widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password" , widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username' , 'first_name','last_name' ,'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password']!=data['password2']:
            raise forms.ValidationError("Your passwords don't match")
        return data['password2']

class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name" , "last_name", "email"]

class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['birthday' , 'photo']