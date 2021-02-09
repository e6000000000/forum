from django.views.generic import UpdateView, DetailView, UpdateView
from django_registration.backends.activation.views import RegistrationView
from django.urls import reverse_lazy

from . import models
from core.views import BaseView
from .models import User


class ProfileDetailView(BaseView, DetailView):
    """
    Display a `auth.User` model.
    """
    model = User
    context_object_name = 'account'
    template_name = 'accounts/profile.html'


class ProfileUpdateView(BaseView, UpdateView):
    """
    Display form to update a `auth.User` model.
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
