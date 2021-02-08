from typing import Any
from django.contrib.auth import get_user_model

from .exceptions import *
from .models import *


User = get_user_model()


def forum_search(text: str) -> dict:
    """
    Search `forum.Section`, `forum.Thread` and `auth.User` models in database

    Args:
        text: str - text to search for
    
    Return:
        {
            'sections': [...],
            'threads': [...],
            'accounts': [...],
        }
    """
    
    result = {}

    result['sections'] = Section.objects.filter(
        title__unaccent__lower__trigram_similar=text
    )
    result['sections'] = result['sections'].union(
        Section.objects.filter(
            description__search=text
        )
    )

    result['threads'] = Thread.objects.filter(
        title__unaccent__lower__trigram_similar=text
    )

    result['accounts'] = User.objects.filter(
        username__unaccent__lower__trigram_similar=text
    )
    result['accounts'] = result['accounts'].union(
        User.objects.filter(
            first_name__unaccent__lower__trigram_similar=text
        )
    )
    result['accounts'] = result['accounts'].union(
        User.objects.filter(
            last_name__unaccent__lower__trigram_similar=text
        )
    )

    return result


def toggle_thread_is_closed(pk: Any, user: User) -> Thread:
    """
    Toggle `is_closed` bool variable of `forum.Thread` if user have permissions.

    Args:
        pk: Any - primary key of `forum.Thread` model
        user: User - user who wants to toggle. if `None` it allows.
    Return:
        `forum.Thread` model which was changed
    """

    thread = Thread.objects.get(
        pk=pk
    )
    if user is not None and thread.author != user:
        raise PermissionsDenied()

    thread.is_closed = not thread.is_closed
    thread.save()

    return thread