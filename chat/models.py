from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    name = models.TextField()

    def __str__(self):
        return '%s' % self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, models.CASCADE, related_name='message')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return '%s(%s)' % (self.message, self.room.name)