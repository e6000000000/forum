from django.views.generic import UpdateView, DetailView
from django.contrib.auth.models import User


class ProfileDetailView(DetailView):
    """
    Display a :model:`auth.User`.
    """
    model = User
    context_object_name = 'account'
    template_name = 'accounts/profile.html'
