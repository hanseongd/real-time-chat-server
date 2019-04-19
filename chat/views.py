import json

from django.shortcuts import render

# Create your views here.
from django.utils.safestring import mark_safe

from chat.models import Message


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    messages = list(Message.objects.filter(room__name=room_name).extra(
        select={'created_at': 'DATETIME(created_at)'}
    ).values('message', 'created_at'))

    return render(request, 'chat/room.html', {
        'room_name': json.dumps(room_name),
        'messages': messages
    })
