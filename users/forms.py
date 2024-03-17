from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from users.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }),
                               error_messages={
                                   "required": "Пожалуйста, введите имя пользователя!"

                               },
                               )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }),
                               error_messages={
                                   "required": "Пожалуйста, введите пароль!"
                               },
                               )

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegistrationForm(UserCreationForm):
    CHOICES = {'1': "Муж.", '2': "Жен."}
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={
        "required": "Пожалуйста, введите имя!"
    }, )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={
        "required": "Пожалуйста, введите фамилию!"
    }, )
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={
        "required": "Пожалуйста, введите имя пользователя!",
        'unique': "Пользователь с таким именем уже существует!"
    }, )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), error_messages={
        "required": "Пожалуйста, введите пароль!!",
        "help_text": "Минимальная длинна пароля - 8 символов",
        "password_mismatch": "The two password fields "
    }, )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', }), error_messages={
        "required": "Пожалуйста, повторите пароль!!"
    }, )
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '13'}), error_messages={
        "required": "Пожалуйста, введите номер телефона!"
    }, )
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'example@email.com', }), error_messages={
        "required": "Пожалуйста, введите email адрес!",
        "invalid": "Введите email адрес в формате example@email.ru"
    }, )

    # gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'form-check-input', }), choices=CHOICES)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'phone', 'email',)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', forms.ValidationError(
                "Не совпадают",
                code='password_mismatch',
            ))


class UserProfileForm(UserChangeForm):
    CHOICES = {"0": "Муж.", "1": "Жен."}
    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),
    }
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-label'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-label'}))
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control-label', 'maxlength': '13', 'readonly': True}),
        error_messages={
            "required": "Пожалуйста, введите номер телефона!"
        }, )
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control-label', }),
        error_messages={
            "required": "Пожалуйста, введите email адрес!",
            "invalid": "Введите email адрес в формате example@email.ru"
        }, )
    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'btn-check'}), required=False,
                               choices=CHOICES, )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'instance' in kwargs:
            initial['gender'] = str(kwargs['instance'].gender)  # Предположим, что пол хранится как строка
        kwargs['initial'] = initial
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'gender')
