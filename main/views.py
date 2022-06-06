from django.shortcuts import render
from accounts.models import *
from club.models import *
# Create your views here.

def index(request):
    user_id = request.session.get('user')
    print(user_id)
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        letters = Letter.objects.filter(to_member_name=member.name, is_read=False)
        print(letters)
        return render(request, 'main.html', {'member':member, 'letters_num':len(letters)})
    return render(request, 'main.html')

def chatbot(request):
    return render(request, 'chatbot.html')
