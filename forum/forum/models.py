from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    """Stores a section of forum,
    related to :model:`auth.User`
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    raiting = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title

class Thread(models.Model):
    """Stores a thread of section,
    related to :model:`auth.User` and :model:`forum.Section`
    """
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    raiting = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='threads', related_query_name="thread")

    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title

class Post(models.Model):
    """Stores a forum thread,
    related to :model:`auth.User` and :model:`forum.Section`
    """
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    reply_to = models.ForeignKey(
        'Post',
        on_delete=models.SET_NULL,
        related_name='replys',
        related_query_name="reply",
        null=True,
        blank=True
    )
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts', related_query_name='post')

    def __str__(self):
        return self.text
    def __repr__(self):
        return self.text