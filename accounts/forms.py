from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group
from django.core import validators


class RegisterForm(UserCreationForm):
    """Form to register the user. Custom form is used to collect the username
    and email for registration"""
    email = forms.EmailField(max_length=100, help_text='Required a valid email')
    developer = forms.BooleanField(label='Register as developer', required=False)
    description = forms.CharField(widget=forms.Textarea)
    nickname = forms.CharField(max_length=20, help_text='Max length 20 characters')
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password1', 'password2', 'description', 'image')


class GroupChoiceForm(forms.Form):
    """GroupChoiceForm is used to register group - basically for the user who
    uses social login"""
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)


class ProfileUpdateForm(RegisterForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['developer']
