from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import Member

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
            user.is_active = False
            user.save()

            # member 정보 입력
            name = request.POST['name']
            email=request.POST['email']
            student_num=request.POST['student_num']
            phone_num=request.POST['phone_num']
            member = Member(name=name, email=email, student_num=student_num, phone_num=phone_num)
            member.user=user
            member.save()
            #auth.login(request, user)
            #request.session['user'] = user.id
            #return redirect('/')

            current_site = get_current_site(request)
            message = render_to_string(
                'activation_email.html',
                {'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
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
        print(user)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = user.id
            return redirect('/')
        # elif user.is_active == False:
        #     return render(request, 'login.html', {'error':'계정이 활성화 되지 않았습니다. 계정에 등록된 학교 이메일 주소를 인증해 주세요.'})
        else:
            context = {
                'error1':'아이디 혹은 비밀번호가 잘못되었습니다.',
                'error2':'계정이 활성화 되지 않았습니다. 계정에 등록된 학교 이메일 주소를 인증해 주세요.'
            }
            return render(request, 'login.html', context)

    else:
        return render(request, 'login.html')

# 로그아웃 view
def logout(request):
    auth.logout(request)
    return redirect('/')

# 계정 활성화 view(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('/')
    else:
        #return render(request, 'main.html', {'error':'계정 활성화 오류'})
        return redirect('main:index', {'error':'계정 활성화 오류'}) 