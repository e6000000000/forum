from django.views.generic import DetailView, UpdateView
from django_registration.backends.activation.views import RegistrationView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from . import models
from core.views import BaseView


User = get_user_model()


class ProfileDetailView(BaseView, DetailView):
    """
    Display `User`.
    """
    model = User
    context_object_name = 'account'
    template_name = 'accounts/profile.html'


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
        'email',
        'bio',
        'avatar',
    ]

    def get_object(self):
        return self.request.user
