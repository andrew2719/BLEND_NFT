from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods

from User.models import CustomUser as User

def index(request):
    return redirect('login')

def register(request):
    if request.method =='POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        wallet_id = request.POST.get('wallet_id')
        user = User.objects.create_user(email=email,first_name=first_name,last_name=last_name,password=password,wallet_id=wallet_id)
        user.save()
        return redirect('login')
    return render(request,'register.html')

def login_(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')

def logout_(request):
    logout(request)
    return redirect('login')

def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request,'home.html')
    else:
        return redirect('login')

def test_api(request):
    data = [{'name':'Test', 'by': 'John Doe', 'description':'This is a test API', 'price': 0.8}]
    return JsonResponse({'data':data})
