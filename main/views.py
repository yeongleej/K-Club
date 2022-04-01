from django.shortcuts import render
from accounts.models import *
# Create your views here.

def index(request):
    user_id = request.session.get('user')
    print(user_id)
    if user_id:
        user = User.objects.get(pk=user_id)
        member = Member.objects.get(user=user)
        return render(request, 'main.html', {'member':member})
    return render(request, 'main.html')