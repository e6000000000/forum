from django_registration.forms import RegistrationForm

from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV2Invisible, ReCaptchaV3


User = get_user_model()

class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = [
            'username',
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            'password1',
            'password2',
        ]

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'dark',
            }
        )
    )