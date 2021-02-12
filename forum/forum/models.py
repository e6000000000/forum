from django.db import models
from django.db.models import functions
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


models.CharField.register_lookup(functions.Lower)
models.TextField.register_lookup(functions.Lower)

User = get_user_model()


class Section(models.Model):
    """
    Section of forum,
    related to `accounts.User` model

    It will be looks like:
        section1 (about something)
        section2 (about something else)
    """

    title = models.CharField(
        verbose_name='Title',
        max_length=100,
        unique=True
    )
    description = models.TextField(
        verbose_name='Description',
        max_length=500
    )
    author = models.ForeignKey(
        verbose_name='Author',
        to=User,
        on_delete=models.CASCADE,
        null=True
    )
    likers = models.ManyToManyField(
        verbose_name='Likers',
        to=User,
        related_name='liked_sections'
    )
    creation_datetime = models.DateTimeField(
        verbose_name='Creation date and time',
        auto_now_add=True
    )

    def get_absolute_url(self):
        return reverse_lazy(
            'section_details',
            kwargs={
                'pk': self.pk,
            }
        )

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title

class Thread(models.Model):
    """Thread in Section,
    related to `accounts.User` and `forum.Section` model

    It will be looks like:
        section1
        |---thread1 (help me with ...)
        |---thread2 (how to ...)
    """

    title = models.CharField(
        verbose_name='Title',
        max_length=100,
        unique=True
    )
    author = models.ForeignKey(
        verbose_name='Author',
        to=User,
        on_delete=models.CASCADE,
        null=True
    )
    likers = models.ManyToManyField(
        verbose_name='Likers',
        to=User,
        related_name='liked_threads'
    )
    is_closed = models.BooleanField(
        verbose_name='Is closed',
        default=False
    )
    creation_datetime = models.DateTimeField(
        verbose_name='Creation date and time',
        auto_now_add=True
    )
    section = models.ForeignKey(
        verbose_name='Section',
        to=Section,
        on_delete=models.CASCADE,
        related_name='threads',
        related_query_name="thread"
    )

    def get_absolute_url(self):
        return reverse_lazy(
            'thread_details',
            kwargs={
                'section_pk': self.section.pk,
                'pk': self.pk,
            }
        )

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title

class Post(models.Model):
    """Post in Thread,
    related to `accounts.User` model and `forum.Section` model

    It will be looks like:
        thread1
        |---post1 (created with thread creation,
        |          there user will describe his question)
        |---post2 (reply to first post)
        |---post3 (reply to one of posts above)
    """

    text = models.TextField(
        verbose_name='Text',
        max_length=2000
    )
    author = models.ForeignKey(
        verbose_name='Author',
        to=User,
        on_delete=models.CASCADE,
        null=True
    )
    creation_datetime = models.DateTimeField(
        verbose_name='Creation date and time',
        auto_now_add=True
    )
    reply_to = models.ForeignKey(
        verbose_name='Reply to',
        to='Post',
        on_delete=models.SET_NULL,
        related_name='replys',
        related_query_name="reply",
        null=True,
        blank=True
    )
    thread = models.ForeignKey(
        verbose_name='Thread',
        to=Thread,
        on_delete=models.CASCADE,
        related_name='posts',
        related_query_name='post'
    )

    def get_absolute_url(self):
        return self.thread.get_absolute_url()
    
    def __str__(self):
        return self.text
    def __repr__(self):
        return self.text