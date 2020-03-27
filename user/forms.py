from django import forms
from .models import user_additional_info, User


class user_signup_form(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lastname'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isupper():
            raise forms.ValidationError('username must be in lower case')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(User.objects.filter(email=email))
        if User.objects.filter(email=email):
            raise forms.ValidationError("email already in use")
        return email


class user_additional_info_form(forms.ModelForm):
    class Meta():
        model = user_additional_info
        fields = ['profile_pic', 'bio']
        # exclude = ['user']
        widgets = {
            # 'profile_pic': forms.ImageField(),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'bio (optional)'}),

        }
