from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import Member
from club.models import *

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token

# Create your views here.

# 회원가입 view
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            user.save()

            # member 정보 입력
            name = request.POST['name']
            email=request.POST['email']
            if "koreatech.ac.kr" in email:
                pass
            else:
                return render(request, 'signup.html', {'error': '학교 메일을 입력해주세요.'})
            student_num=request.POST['student_num']
            major = request.POST['major']
            phone_num=request.POST['phone_num']
            member = Member(name=name, email=email, major=major, student_num=student_num, phone_num=phone_num)
            member.user=user
            member.save()

            current_site = get_current_site(request)
            message = render_to_string(
                'activation_email.html',
                {'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
                }
            )
            mail_title = "K-Club 계정 활성화 확인 이메일"
            mail_to = request.POST['email']
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

# 로그인 view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            mem = Member.objects.get(user=user)
            if mem.is_auth == False:
                return render(request, 'login.html', {'error':'계정이 활성화 되지 않았습니다. 계정에 등록된 학교 이메일 주소를 인증해 주세요.'})
            
            auth.login(request, user)
            request.session['user'] = user.id
            return redirect('/')
        else:
            return render(request, 'login.html', {'error':'아이디 혹은 비밀번호가 잘못되었습니다.'})
    else:
        return render(request, 'login.html')

# 로그아웃 view
def logout(request):
    auth.logout(request)
    return redirect('/')

# 계정 활성화 view(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        #uid = force_str(urlsafe_base64_decode(uidb64))
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        a_mem = Member.objects.get(user=user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        #user = None
        a_mem.is_auth = False

    if user is not None and account_activation_token.check_token(user, token):
        #user.is_active = True
        #user.save()
        a_mem.is_auth = True
        a_mem.save()
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'main/main.html', {'error':'계정 활성화 오류'})

def password_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('accounts:mypage')
        else:
            return render(request, 'password_check.html', {'error':'잘못된 비밀번호 입니다.'})
    return render(request, 'password_check.html')


def mypage(request):
    user_id = request.session.get('user')
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        clubs = Club.objects.filter(member=member)
        if request.method == 'POST':
            member.name = request.POST['name']
            member.major = request.POST['major']
            member.phone_num = request.POST['phone_num']
            member.save()
            return redirect('accounts:mypage')
        if clubs == None:
            return render(request, 'mypage.html', {'member':member})
        return render(request, 'mypage.html', {'member':member, 'clubs':clubs})
    return render(request, 'main.html')

def application_list(request, cName):
    # club = Club.objects.filter(name=cName)
    apps = Application.objects.filter(club_name = cName)
    if request.method == 'POST':
        result = request.POST['result']
        sNum = request.POST['student_num']
        member = Member.objects.get(student_num = sNum)
        app = Application.objects.get(member = member)
        if result == '승인':
            new_club = Club(name=cName, member=member)
            new_club.save()
            app.delete()
        else:
            app.delete()
        return redirect('accounts:application_list', cName=cName)
    return render(request, 'application_list.html', {'applications':apps, 'cName':cName, 'appsLen':len(apps)})

def club_member_management(request, cName):
    clubs = Club.objects.filter(name=cName)
    if request.method == 'POST':
        result = request.POST['result']
        club_id = request.POST['club_id']
        club = Club.objects.get(id=club_id)
        if result == '관리자 권한 부여':
            club.is_manager = True
            club.save()
        elif result == '관리자 권한 삭제':
            club.is_manager = False
            club.save()
            if request.user == club.member.user:
                return redirect('/')
        else:
            if request.user == club.member.user:
                club.delete()
                return redirect('/')
        return redirect('accounts:club_member_management', cName=cName)
    return render(request, 'club_member_management.html', {'clubs':clubs, 'cName':cName, 'clubsLen':len(clubs)})

def club_resign(reuqest, id):
    club = Club.objects.get(id=id)
    club.delete()
    return redirect('accounts:mypage')