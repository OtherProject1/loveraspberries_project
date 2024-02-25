from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegistrationForm(AuthenticationForm):
    CHOICES = {'1': "Муж.", '2': "Жен."}
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13'}))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'example@email.com', }))
    # gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-input', }), choices=CHOICES)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'phone', 'email',)
