from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView

from . import views
from . import forms


urlpatterns = [
    path(
        'register/',
        RegistrationView.as_view(
            form_class=forms.CustomUserForm
        ),
        name='django_registration_register'
    ),
    path(
        '',
        include('django_registration.backends.activation.urls')
    ),
    path(
        '',
        include('django.contrib.auth.urls')
    ),
    path(
        'profile/<int:pk>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'profile_edit/',
        views.ProfileUpdateView.as_view(),
        name='profile_edit'
    ),
]