from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    name = models.TextField()
    slug = models.SlugField(unique=True)


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, models.CASCADE, related_name='message')
