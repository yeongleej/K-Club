from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
import json
from accounts.models import *
from chat.models import *

# Create your views here.

def chat_main(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        return render(request, "chat_main.html", {'username':member.name})
    return render(request, "chat_main.html")


@login_required
def room(request, room_name):
    cur_member = Member.objects.get(user=request.user)
    if cur_member:
        # cur_member.room = room_name
        # cur_member.save()
        #chat_members = Member.objects.filter(room=room_name)
        messages = Message.objects.filter(room=room_name)
        return render(request, 'room.html', {
            'room_name_json': mark_safe(json.dumps(room_name, ensure_ascii=False)),
            'username': mark_safe(json.dumps(request.user.username, ensure_ascii=False)),
            # 'chat_members':  chat_members,
            'messages' : messages,
        })
    else:
        return redirect("accounts:login")


# @login_required
# def chatbot(request):
#     return render(request, "chatbot.html")
# def chatbot(request):
#     room_name = chatbot
#     cur_member = Member.objects.get(user=request.user)
#     if cur_member:
#         # cur_member.room = room_name
#         # cur_member.save()
#         #chat_members = Member.objects.filter(room=room_name)
#         messages = Message.objects.filter(room=room_name)
#         return render(request, 'room.html', {
#             'room_name_json': mark_safe(json.dumps(room_name, ensure_ascii=False)),
#             'username': mark_safe(json.dumps(request.user.username, ensure_ascii=False)),
#             # 'chat_members':  chat_members,
#             'messages' : messages,
#         })
#     else:
#         return redirect("accounts:login")

