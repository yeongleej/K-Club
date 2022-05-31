from contextlib import redirect_stderr
from unicodedata import name
from django.shortcuts import render, redirect
from .models import *
from accounts.models import Member

# Create your views here.

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
            if club.is_manager: is_manager = True
    return render(request, 'notice_index.html', {'boards': boards, 'topic':t, 'is_manager':is_manager})

def board_create(request, topic):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        if len(clubs) == 0: return redirect('club:club_list')
        if request.method == 'POST':
            new_board = Board()
            new_board.member = member
            new_board.club_name = request.POST['club']
            new_board.topic = topic
            new_board.title = request.POST['title']
            new_board.content = request.POST['content']
            new_board.save()
            if topic == 'free': return redirect('club:freeBoard_index')
            elif topic == 'info': return redirect('club:infoBoard_index')
            elif topic == 'promo': return redirect('club:promoBoard_index')
            else: return redirect('main:index')
        else:
            return render(request, 'board_create.html', {'topic':topic, 'member':member, 'clubs':clubs})
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
    return render(request, 'board_detail.html', {'board':board, 'comments':comments})

def comment_delete(request, id):
    comment = Comment.objects.get(id=id)
    board = comment.board
    comment.delete()
    return redirect('club:board_detail', board.id)

def board_update(request, id):
    board = Board.objects.get(id=id)
    member = Member.objects.get(id=board.member.id)
    clubs = Club.objects.filter(member=member)
    if request.method == 'POST':
        board.title = request.POST['title']
        board.club_name = request.POST['club']
        board.content = request.POST['content']
        board.save()
        return render(request, 'board_detail.html', {'board':board})
    return render(request, 'board_update.html', {'board':board, 'clubs':clubs, 'member':member})

def board_delete(request, id):
    board = Board.objects.get(id=id)
    topic = board.topic
    board.delete()
    if topic == 'free': return redirect('club:freeBoard_index')
    elif topic == 'info': return redirect('club:infoBoard_index')
    elif topic == 'promo': return redirect('club:promoBoard_index')
    else: return redirect('main:index')

def board_index(request, topic):
    if topic == 'free': return redirect('club:freeBoard_index')
    elif topic == 'info': return redirect('club:infoBoard_index')
    elif topic == 'promo': return redirect('club:promoBoard_index')
    else: return redirect('main:index')

def event(request):
    return render(request, 'event.html')


def club_list(request):
    clubs = Club.objects.values_list('name', flat=True).distinct()
    return render(request, 'club_list.html', {'clubs': clubs})

def myClub_list(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        return render(request, 'myClub_list.html', {'clubs':clubs})
    return redirect('accounts:login')

def club_home(request, cName):
    return render(request, 'club_home.html', {'cName': cName})

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