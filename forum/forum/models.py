from django.db import models
from django.contrib.auth.models import AnonymousUser, User


class Section(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=AnonymousUser)
    raiting = models.IntegerField()
    creation_datetime = models.DateTimeField(auto_now_add=True)

class Thread(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=AnonymousUser)
    raiting = models.IntegerField()
    is_closed = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='threads', related_query_name="thread")

class Post(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=AnonymousUser)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    reply_to = models.ForeignKey(
        'Post',
        on_delete=models.SET_DEFAULT,
        related_name='replys',
        related_query_name="reply"
    )
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts', related_query_name='post')