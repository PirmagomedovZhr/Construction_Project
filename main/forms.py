
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['position']


class PositionAuthenticationForm(AuthenticationForm):
    position = forms.CharField(max_length=20, widget=forms.Select(choices=UserProfile.POSITION_CHOICES))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['position'].widget.attrs.update({'class': 'form-control'})


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "Email",
            'placeholder': "Имя пользователя"
        }),
    )
    position = forms.ChoiceField(
        choices=[
            ('architect', 'Архитектор'),
            ('constructor', 'Конструктор'),
            ('designer', 'Дизайнер')
        ],
        widget=forms.Select(attrs={
            'class': "form-control mt-2",
            'id':'position'
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "password",
            'placeholder': "Пароль"
        }),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "repassword",
            'placeholder': "Повторите пароль"
        }),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control mt-2",
            'id': "first_name",
            'placeholder': "Имя"
        }),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control mt-2",
            'id': "last_name",
            'placeholder': "Фамилия"
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )


    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Имя пользователя"
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
            'placeholder': "Пароль"
        })

    )