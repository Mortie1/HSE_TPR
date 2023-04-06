from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
    

from django.utils.translation import gettext_lazy as _


class UserCacheMixin:
    user_cache = None

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        label=_('Email'),
        help_text=_('Required. Enter an existing email address.'),
        widget=forms.EmailInput(attrs={'class':"password", 'placeholder': "Адрес Эл. почты"}),
        error_messages={'required': 'This is a custom error message for #862'}
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':"password", 'placeholder': "Пароль"}),
        help_text=password_validation.password_validators_help_text_html(),
        error_messages={'required': 'This is a custom error message for #862'},
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':"password", 'placeholder': "Повторите Пароль"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':"password", 'placeholder': "Иван"}),
            'last_name': forms.TextInput(attrs={'class':"password", 'placeholder': "Иванов"}),
        }
        

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError('Этот адрес эл. почты уже зарегистрирован.')

        return email
    
    
    
class LoginForm(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'class':"password", 'placeholder': "Пароль"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False, widget=forms.CheckboxInput(attrs={'class':"custom-checkbox"}))

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError('Вы ввели неверный пароль.')

        return password
    
class EmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class':"password", 'placeholder': "Адрес Эл. почты"}))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError('Вы ввели неверный адрес эл. почты.')

        if not user.is_active:
            raise ValidationError('Этот аккаунт не активирован.')

        self.user_cache = user

        return email
    
    
class LoginViaEmailForm(LoginForm, EmailForm):
    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']


class ChangePasswordForm(SetPasswordForm):
    
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class':"password", 'placeholder': "Введите старый пароль"}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':"password", 'placeholder': "Новый пароль"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':"password", 'placeholder': "Повторите новый пароль"}),
    )
    
class ChangeNameForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget = forms.TextInput(attrs={'class':"password", 'placeholder': "Введите ваше имя"}))
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget = forms.TextInput(attrs={'class':"password", 'placeholder': "Введите вашу фамилию"}))
        

class CustomSetPasswordForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Новый пароль"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Повторите новый пароль"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user