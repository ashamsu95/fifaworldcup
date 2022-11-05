from django import forms
from django.forms import ModelForm
from .models import MyUser
from django.contrib.auth import get_user_model

User=get_user_model

class phone(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class Team(ModelForm):
    class Meta:
        model = MyUser
        fields = ['team']
        

class LoginForm(forms.Form):
    Email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    First_Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Last_Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password_first = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # team_field = forms.ChoiceField(Team())
    # team_field= forms.CharField(required=False, widget=forms.Select(choices=MyUser.team,attrs={'class': 'form-control'} ))
    #team_field = forms.ModelChoiceField(queryset=MyUser.objects.all(), initial=0)
    team_field = Team()
    def clean(self):
        cleaned_data = self.cleaned_data
        password_one = self.cleaned_data.get('password_first')
        password_two = self.cleaned_data.get('password_again')
        if password_one != password_two:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def clean_email(self):
        email_address = self.cleaned_data.get('email')
        qs = get_user_model().objects.filter(email=email_address)
        if qs.exists():
            raise forms.ValidationError("The email address you've chosen is already registered.")
        return email_address

