from django import forms
from .models import User


class user_signup_form(forms.ModelForm):
    class Meta:
        model = User
        # fields = ['username', 'first_name', 'last_name', 'password', 'email']
        fields = '__all__'
        # fields = ('username', 'first_name', 'last_name', 'password', 'email')

    # def __init__(self, *args, **kwargs):
    #     super(user_signup_form, self).__init__(*args, **kwargs)
    #     self.fields.widget.attrs = {'class': 'form-control'}
