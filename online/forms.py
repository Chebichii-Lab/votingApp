from online.models import Poll, Profile, Choice
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# The signup form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'picture', 'bio']

class AddPollForm(forms.ModelForm):

    # choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['description']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }

class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['description']
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),}


class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }