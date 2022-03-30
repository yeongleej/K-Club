from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from accounts.models import *

# Create your views here.

def index(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        return render(request, "chat_main.html", {'username':member.name})
    return render(request, "chat_main.html")

def room(request, room_name):
    #user_id = request.session.get('user')
    #if user_id:
    #    user = User.objects.get(pk=user_id)
    #    member = Member.objects.get(user=user)
    #    return render(request, "room.html", {
    #        'room_name_json': mark_safe(json.dumps(room_name)),
    #        'member':member
    #    })
    return render(request, "room.html", {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

