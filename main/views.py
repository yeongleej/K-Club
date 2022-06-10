from django.shortcuts import render
from accounts.models import *
from club.models import *
# Create your views here.

def index(request):
    user_id = request.session.get('user')
    boards = Board.objects.filter(topic__in =['free', 'info', 'promo'])
    notices = Board.objects.filter(topic='notice')
    clubs_info = Club_Info.objects.all()
    boardsList = []
    noticesList = []
    clubsList = []
    i = 0
    for board in boards:
        if (i == 8): break
        boardsList.append(board)
        i += 1
    j = 0
    for notice in notices:
        if(j == 8): break
        noticesList.append(notice)
        j += 1
    k = 0
    for club in clubs_info:
        if(k==15): break
        clubsList.append(club)
        k += 1
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        letters = Letter.objects.filter(to_member_name=member.name, is_read=False)

        return render(request, 'main.html', {'member':member, 'letters_num':len(letters), 'boards':boardsList, 'notices':noticesList, 'clubs_info':clubsList,})
    return render(request, 'main.html', {'boards':boardsList, 'notices':noticesList, 'clubs_info':clubsList,})

def chatbot(request):
    return render(request, 'chatbot.html')
