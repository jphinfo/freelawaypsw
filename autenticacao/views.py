from re import U
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/plataforma')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/auth/cadastro')

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')
        
        user = User.objects.filter(username = username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'usuario já existe')
            return redirect('/auth/cadastro')

        try:

            user = User.objects.create_user(username=username, password=password)
            user.save()

            return redirect('/auth/logar')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')

def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/plataforma')

        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Invalid username or password')
            return redirect('/auth/logar')

        else:
            auth.login(request, user)
            return redirect('/plataforma')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')