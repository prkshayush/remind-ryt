from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import speech_recognition as sr
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import *
from .forms import GroupForm


# authentication
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'User does not exist')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect')

        context = {'page': page}
        return render(request, 'base/authentication.html', context)
    
def logOutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form, 'page': page}
    return render(request, 'base/authentication.html', context)


# functions
def home(request):
    groups = Group.objects.all()
    group_count = groups.count()

    context = {'groups': groups, 'group_count': group_count,}
    return render(request, 'base/home.html', context)

def group(request, key):
    group = Group.objects.get(id=key)
    group_messages = group.message_set.all()
    participants = group.participants.all()
    
    context = {'group': group, 'group_messages': group_messages, 'participants': participants}

    return render(request, 'base/group.html', context)

# create group
@login_required(login_url='/login')
def createGroup(request):
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        Group.objects.create(
            host = request.user,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/create-group.html', context)

@login_required(login_url='/login')
def joinGroup(request, key):
    group = get_object_or_404(Group, id=key)

    group.participants.add(request.user)
    
    return redirect('group', key=group.id)

# speech recorgnizer
@login_required(login_url='/login')
@csrf_exempt
def process_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio_data']
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        return JsonResponse({'text': text})