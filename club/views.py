from contextlib import redirect_stderr
from re import S
from turtle import fd
from unicodedata import name
from django.shortcuts import render, redirect
from .models import *
from accounts.models import Member
import json
from datetime import datetime, date

# Create your views here.
def board_index(request, topic):
    if topic == 'free': return redirect('club:freeBoard_index')
    elif topic == 'info': return redirect('club:infoBoard_index')
    elif topic == 'promo': return redirect('club:promoBoard_index')
    else: return redirect('main:index')

def freeBoard_index(request):
    t = 'free'
    try:
        boards = Board.objects.filter(topic=t)
    except Board.DoesNotExist:
        boards = None
    return render(request, 'freeBoard_index.html', {'boards': boards, 'topic':t})

def infoBoard_index(request):
    t = 'info'
    try:
        boards = Board.objects.filter(topic=t)
    except Board.DoesNotExist:
        boards = None
    return render(request, 'infoBoard_index.html', {'boards': boards, 'topic':t})

def promoBoard_index(request):
    t = 'promo'
    try:
        boards = Board.objects.filter(topic=t)
    except Board.DoesNotExist:
        boards = None
    return render(request, 'promoBoard_index.html', {'boards': boards, 'topic':t})

def notice_index(request):
    t = 'notice'
    is_manager = False
    try:
        boards = Board.objects.filter(topic=t)
    except Board.DoesNotExist:
        boards = None
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        # 유저가 가입한 여러 동아리중 한 개이상의 동아리에서 관리자 권한을 가지고 있으면 공지사항 등록 가능
        for club in clubs:
            if club.is_manager: 
                is_manager = True
                break
    return render(request, 'notice_index.html', {'boards': boards, 'topic':t, 'is_manager':is_manager})

def board_create(request, topic):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        # clubs = Club.objects.filter(member=member)
        # if len(clubs) == 0: return redirect('club:club_list')
        if request.method == 'POST':
            new_board = Board()
            new_board.member = member
            # new_board.club_name = request.POST['club']
            new_board.topic = topic
            new_board.title = request.POST['title']
            new_board.content = request.POST['content']
            new_board.save()
            if topic == 'free': return redirect('club:freeBoard_index')
            elif topic == 'info': return redirect('club:infoBoard_index')
            elif topic == 'promo': return redirect('club:promoBoard_index')
            elif topic == 'notice': return redirect('club:notice_index')
            else: return redirect('main:index')
        else:
            return render(request, 'board_create.html', {'topic':topic, 'member':member, 'cName':None})
    return redirect('accounts:login')

def board_detail(request, id):
    board = Board.objects.get(id=id)
    board.views += 1
    board.save()
    comments = Comment.objects.filter(board=board)
    if request.method == 'POST':
        user_id = request.session.get('user')
        if user_id:
            user = User.objects.get(pk=user_id)
            member = Member.objects.get(user=user)
            comment = Comment()
            comment.board = board
            comment.member = member
            comment.comment = request.POST['comment']
            comment.save()
            board.views -= 2
            board.save()
            return redirect('club:board_detail', board.id)
        return render(request, 'board_detail.html', {'board':board, 'comments':comments ,'error':'로그인 하세요!'})
    return render(request, 'board_detail.html', {'board':board, 'comments':comments, 'cName':board.club_name})

def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    board = comment.board
    comment.delete()
    return redirect('club:board_detail', board.id)

def board_update(request, id):
    board = Board.objects.get(id=id)
    member = Member.objects.get(id=board.member.id)
    if request.method == 'POST':
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.save()
        return render(request, 'board_detail.html', {'board':board})
    return render(request, 'board_update.html', {'board':board, 'member':member})

def board_delete(request, id):
    board = Board.objects.get(id=id)
    topic = board.topic
    cName = board.club_name
    board.delete()
    if topic == 'free': return redirect('club:freeBoard_index')
    elif topic == 'info': return redirect('club:infoBoard_index')
    elif topic == 'promo': return redirect('club:promoBoard_index')
    elif topic == 'notice': return redirect('club:notice_index')
    elif topic == 'club': return redirect('club:club_board_index', cName)
    else: return redirect('main:index')

def event_calendar(request):
    events = Schedule.objects.all()
    eventdict = dict()
    i = 0
    for event in events:
        eventdict["club_name"+str(i)] = event.club_name
        eventdict["title"+str(i)] = event.title
        eventdict["start_at"+str(i)] = event.start_at
        i += 1
    print(eventdict)
    eventsJson = json.dumps(eventdict, default=str, ensure_ascii=False)
    return render(request, 'event_calendar.html', {'events':events, 'eventsJson':eventsJson})

def schedules_sync(request):
    today = date.today()
    schedules = Schedule.objects.all()
    for schedule in schedules:
        sDate = schedule.start_at
        fDate = schedule.finish_at
        if today > fDate: schedule.state = "마감"
        if today < sDate: schedule.state = "진행전"
        if sDate <= today and fDate >= today: schedule.state  = "진행중"
        schedule.save()
    return redirect('club:event_calendar')

def event_thisMonth(request):
    ty = str(date.today().year)
    tm= date.today().month
    if (tm < 10): tm = '0'+ str(tm)
    else: tm = ''+ str(tm)
    try:
        schedules = Schedule.objects.filter(start_at__year=ty, start_at__month=tm)
    except Schedule.DoesNotExist:
        schedules = None   
    return render(request, 'event_thisMonth.html', {'schedules':schedules})

def club_list(request):
    clubs_info = Club_Info.objects.all()
    #clubs = Club.objects.values_list('name', flat=True).distinct()
    return render(request, 'club_list.html', {'clubs_info': clubs_info})

def myClub_list(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        return render(request, 'myClub_list.html', {'clubs':clubs})
    return redirect('accounts:login')

def club_home(request, cName):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        try:
            club_info = Club_Info.objects.get(name=cName)
        except Club_Info.DoesNotExist:
            club_info = None
        return render(request, 'club_home.html', {'club_info': club_info, 'member':member})
    return redirect('accounts:login')

def club_board_index(request, cName):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        try:
            boards = Board.objects.filter(club_name=cName)
        except Board.DoesNotExist:
            boards = None
        return render(request, 'club_board_index.html', {'boards': boards, 'member':member, 'cName':cName, 'topic':'club'})
    return redirect('accounts:login')

def club_board_create(request, cName):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        if request.method == 'POST':
            new_board = Board()
            new_board.member = member
            new_board.club_name = cName
            new_board.topic = 'club'
            new_board.title = request.POST['title']
            new_board.content = request.POST['content']
            new_board.save()
            return redirect('club:club_board_index', cName)
        else:
            return render(request, 'board_create.html', {'topic':'club', 'member':member, 'cName':cName})
    return redirect('accounts:login')

def club_application(request, cName):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        for club in clubs:
            if club.name == cName:
                return render(request, 'club_home.html', {'cName': cName})
        if request.method == 'POST':
            sNum = request.POST['student_num']
            try:
                member = Member.objects.get(student_num = sNum)
            except Member.DoesNotExist:
                return render(request, 'application.html', {'cName': cName, 'member':member, 'error': '올바른 정보를 입력하세요.' })
            app = Application(club_name=cName, member=member)
            app.save()
            return redirect('/')
        else:
            return render(request, 'application.html', {'cName': cName, 'member':member})
    return redirect('accounts:login')

def club_schedule_index(request, cName):
    try:
        schedules = Schedule.objects.filter(club_name=cName)
    except Schedule.DoesNotExist:
        schedules = None
    return render(request, 'club_schedule_index.html', {'schedules':schedules, 'cName':cName})

def club_schedule_create(request, cName):
    user_id = request.session.get('user')
    if user_id:
        if request.method == 'POST':
            schedule = Schedule()
            schedule.title = request.POST['title']
            schedule.start_at = request.POST['start_at']
            schedule.finish_at = request.POST['finish_at']
            schedule.content = request.POST['content']
            schedule.image_url = request.FILES['image']
            schedule.club_name = cName
            today = datetime.today()
            sDate =datetime.strptime(schedule.start_at, '%Y-%m-%d')
            fDate =datetime.strptime(schedule.finish_at, '%Y-%m-%d')
            if today > fDate: schedule.state = "마감"
            if today < sDate: schedule.state = "진행전"
            if sDate <= today and fDate >= today: schedule.state  = "진행중"
            schedule.save()
            return redirect('club:club_schedule_index', cName)
        return render(request, 'club_schedule_create.html', {'cName':cName, })
    return redirect('accounts:login')

def club_schedule_detail(request, id):
    schedule = Schedule.objects.get(id=id)
    user_id = request.session.get('user')
    is_club_member = False
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        for club in clubs:
            if club.name == schedule.club_name: 
                is_club_member = True
                break
        return render(request, 'club_schedule_detail.html', {'schedule':schedule, 'is_club_member':is_club_member})
    return redirect('accounts:login')

def club_schedule_update(request, id):
    schedule = Schedule.objects.get(id=id)
    if request.method == 'POST':
        schedule.title = request.POST['title']
        schedule.start_at = request.POST['start_at']
        schedule.finish_at = request.POST['finish_at']
        schedule.content = request.POST['content']
        schedule.image_url = request.FILES['image']
        schedule.save()
        return render(request, 'club_schedule_detail.html', {'schedule':schedule})
    return render(request, 'club_schedule_update.html', {'schedule':schedule})

def club_schedule_delete(request, id):
    schedule = Schedule.objects.get(id=id)
    cName = schedule.club_name
    schedule.delete()
    return redirect('club:club_schedule_index', cName=cName)

def letter_list(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        try:
            send_letters = Letter.objects.filter(from_member_name = member.name)
        except Letter.DoesNotExist:
            send_letters = None
        try:
            receive_letters = Letter.objects.filter(to_member_name= member.name)
        except Letter.DoesNotExist:
            receive_letters = None
        return render(request, 'letter_list.html', {'send_letters':send_letters, 'receive_letters':receive_letters})
    return redirect('accounts:login')

def letter_create(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        try:
            my_letters = Letter.objects.filter(to_member_name = member.name)
        except Letter.DoesNotExist:
            my_letters = None
        if request.method == 'POST':
            try:
                to_member = Member.objects.get(name= request.POST['to_member'])
            except Member.DoesNotExist:
                to_member = None
            if to_member == None: return render(request, 'letter_create.html', {'member':member, 'error':'사용자가 없습니다.'})
            letter = Letter()
            letter.title = request.POST['title']
            letter.from_member_name = member.name
            letter.to_member_name = to_member.name
            letter.content = request.POST['content']
            letter.reference_id = request.POST.get('reference_id', 0)
            letter.save()
            return redirect('club:letter_list')
        return render(request, 'letter_create.html', {'member':member, 'my_letters':my_letters})
    return redirect('accounts:login')

def letter_detail(request, id):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        letter = Letter.objects.get(id=id)
        try:
            reference_letter_id = Letter.objects.get(id=letter.reference_id).id
        except Letter.DoesNotExist:
            reference_letter_id = 0
        all_letters = Letter.objects.all()
        print(reference_letter_id)
        if letter.to_member_name == member.name:
            letter.is_read = True
            letter.save()
        return render(request, 'letter_detail.html', {'member':member, 'letter':letter, 'all_letters':all_letters, 'reference_letter_id':reference_letter_id})
    return redirect('accounts:login')

def letter_delete(request, id):
    letter = Letter.objects.get(id=id)
    letter.delete()
    return redirect('club:letter_list')