from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import Member

# Create your views here.

# 회원가입 view
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            name = request.POST['name']
            email=request.POST['email']
            student_num=request.POST['student_num']
            phone_num=request.POST['phone_num']
            member = Member(name=name, email=email, student_num=student_num, phone_num=phone_num)
            member.user=user
            member.save()
            auth.login(request, user)
            request.session['user'] = user.id
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