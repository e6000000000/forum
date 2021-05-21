from extra_views import InlineFormSet

from .models import Post


class PostInline(InlineFormSet):
    """
    InlineFormSet of `forum.Post` model
    """
    model = Post
    fields = ['text']

    factory_kwargs = {
        'can_delete': False,
        'can_order': False,
        'extra': 1,
    }