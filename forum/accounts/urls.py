from django.urls import path, include

from . import views


urlpatterns = [
    path('', include('django_registration.backends.activation.urls')),
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile'),
]