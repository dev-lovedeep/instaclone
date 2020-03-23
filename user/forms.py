from django import forms
from .models import user_additional_info, User


# class user_signup_form(forms.ModelForm):
#     class Meta:
#         model = user_additional_info
#         # fields = ['username', 'first_name', 'last_name', 'password', 'email']
#         fields = '__all__'
# fields = ('username', 'first_name', 'last_name', 'password', 'email')

# def __init__(self, *args, **kwargs):
#     super(user_signup_form, self).__init__(*args, **kwargs)
#     self.fields.widget.attrs = {'class': 'form-control'}


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


class user_additional_info_form(forms.ModelForm):
    class Meta():
        model = user_additional_info
        fields = ['profile_pic', 'bio']
        # exclude = ['user']
        widgets = {
            # 'profile_pic': forms.ImageField(),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'bio'}),

        }
