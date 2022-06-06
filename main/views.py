from django.shortcuts import render
from accounts.models import *
from club.models import *
# Create your views here.

def index(request):
    user_id = request.session.get('user')
    boards = Board.objects.filter(topic__in =['free', 'info', 'promo'])
    notices = Board.objects.filter(topic='notice')
    clubs_info = Club_Info.objects.all()
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        letters = Letter.objects.filter(to_member_name=member.name, is_read=False)

        return render(request, 'main.html', {'member':member, 'letters_num':len(letters), 'boards':boards, 'notices':notices, 'clubs_info':clubs_info,})
    return render(request, 'main.html', {'boards':boards, 'notices':notices, 'clubs_info':clubs_info,})

def chatbot(request):
    return render(request, 'chatbot.html')
