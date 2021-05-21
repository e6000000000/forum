from django.views.generic import DetailView, UpdateView
from django_registration.backends.activation.views import RegistrationView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import models
from core.exceptions import HttpError
from core.views import BaseView


User = get_user_model()


class ProfileDetailView(BaseView, DetailView):
    """
    Display `User`.
    """
    model = User
    context_object_name = 'account'
    template_name = 'accounts/profile.html'


@method_decorator(login_required, 'dispatch')
class ProfileUpdateView(BaseView, UpdateView):
    """
    Display form to update `User`.
    """
    model = User
    context_object_name = 'account'
    template_name = 'accounts/profile_edit.html'
    fields = [
        'username',
        'first_name',
        'last_name',
        'bio',
        'avatar',
    ]

    def get_object(self):
        return self.request.user
