from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    """
    Custom user registration form.
    Includes validation for email and requires the email field.
    """

    class Meta:
        """
        Meta options for the CreateUserForm.
        Specifies the User model and the fields to include.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and sets the email field as required.
        """
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Email field is required

    def clean_email(self):
        """
        Validates the email field.

        Raises:
            ValidationError: If the email is already in use or too long.

        Returns:
            str: The cleaned email value.
        """
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')

        if len(email) >= 350:
            raise forms.ValidationError('This email is too long.')

        return email


class LoginForm(AuthenticationForm):
    """
    Custom login form.
    Uses custom widgets for username and password fields.
    """
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    """
    Custom user update form.
    Allows updating username and email but excludes password fields.
    """
    password = None  # Password field is excluded

    class Meta:
        """
        Meta options for the UpdateUserForm.
        Specifies the User model and the fields to include.
        """
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and sets the email field as required.
        """
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Email field is required

    def clean_email(self):
        """
        Validates the email field.

        Raises:
            ValidationError: If the email is already in use or too long.

        Returns:
            str: The cleaned email value.
        """
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')

        if len(email) >= 350:
            raise forms.ValidationError('This email is too long.')

        return email

