from typing import Any, Union

from django.contrib.auth import get_user_model

from .exceptions import PermissionsDenied
from .models import Section, Thread, Post
from . import models


User = get_user_model()


def forum_search(text: str) -> dict:
    """
    Search `forum.Section`, `forum.Thread` and `auth.User` in database

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


def toggle_thread_is_closed(pk: Any, user: User=None) -> Thread:
    """
    Toggle `is_closed` bool variable of `forum.Thread` if user have permissions.

    Args:
        pk: Any - primary key of `forum.Thread`
        user: User - user who wants to toggle. if `None` it allows.
    Return:
        `forum.Thread` which was changed
    """

    thread = Thread.objects.get(
        pk=pk
    )
    if user is not None and thread.author.pk != user.pk:
        raise PermissionsDenied()

    thread.is_closed = not thread.is_closed
    thread.save(update_fields=('is_closed', ))

    return thread


def toggle_liked(model_type: str, pk: Any, user: User) -> Union[Section, Thread, Post]:
    """
    Add or remove `User` to likers of `forum.Section` or `forum.Thread`
    
    Args:
        model_type: str - type of model. can be `Section` or `Thread`
        pk: Any - primary key of model instance
        user: User - user who wants to like/unlike.
    
    Return:
        Instance of declarated model_type
    """

    if model_type not in ('Section', 'Thread'):
        raise ValueError(
            f'"model_type" should be in (Section, Thread), not {model_type}'
        )

    model = getattr(models, model_type)
    instance = model.objects.get(pk=pk)
    try:
        instance.likers.get(pk=user.pk)
        instance.likers.remove(user)
    except User.DoesNotExist:
        instance.likers.add(user)

    return instance
