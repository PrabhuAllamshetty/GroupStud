from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


# rooms =[  {'Id':1, 'Name': 'Lets learn Python!'},
#    {'Id':2, 'Name': 'Design with me'},
#    {'Id':3, 'Name': 'Fronend Developers'}]

def LoginPage(request):

    page='Login'

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('Password')
    
        try:
            user = User.objects.get(emial=email)

        except:
            messages.error(request, "User does not exist")
    
        user=authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "Username Or Password does not exist")

    context={'Page': page}
    return render(request, 'Base/login_register.html', context)



def LogoutUser(request):
    logout(request)
    return redirect('Home')


def RegisterPage(request):
    form= MyUserCreationForm
 
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "An Error occured during registration")
    return render(request, 'Base/login_register.html', {'Form': form})


def home(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    topics= Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages= Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {"Rooms":rooms, "Topics": topics, "Room_count": room_count, 'Room_messages':room_messages } 
    return render(request, 'Base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages= room.message_set.all()
    participants = room.participants.all()

    if request.method=="POST":
        message= Message.objects.create(
            user= request.user,
            room= room,
            body= request.POST.get('body') #this body under brackets is the name from room.html file
        )
        room.participants.add(request.user)
        return redirect('Room', pk=room.id)
    context = {'room':room, 'Room_messages': room_messages, 'Participants': participants}
    return render(request, 'Base/room.html', context)

def UserProfile(request,pk):
    user= User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'Rooms': rooms, 'Room_messages':room_messages, 'Topics':topics}
    return render(request, 'Base/profile.html', context)

@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    topics= Topic.objects.all()
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created= Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('Home')
    context = {'Form': form, 'Topics':topics}
    return render(request, 'Base/room_form.html', context)

@login_required(login_url='Login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics= Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        topic_name= request.POST.get('topic')
        topic, created= Topic.objects.get_or_create(name=topic_name)
        room.name= request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('Home')

    context = {"Form":form, 'Topics':topics, 'Room':room}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='Login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == "POST":
        room.delete()
        return redirect('Home')
    return render(request, 'Base/delete.html', {"obj": room})


@login_required(login_url='Login')
def DeleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You cannot delete!!')
    
    if request.method == "POST":
        message.delete()
        return redirect('Home')
    return render(request, 'Base/delete.html', {"obj": message})



@login_required(login_url='Login')
def UpdateUser(request):
    user= request.user
    form = UserForm(instance=user)

    if request.method =='POST':
        form = UserForm(request.POST, request.FILES,  instance= user)
        if form.is_valid:
            form.save()
            return redirect('User-Profile', pk=user.id)
    return render(request, 'Base/update-user.html', {'Form':form})

def TopicsPage(request):
    q= request.GET.get('q') if request.GET.get('q')!= None else ''
    topics= Topic.objects.filter(name__icontains=q)
    return render(request, 'Base/topics.html', {'topics': topics})

def ActivityPage(request):
    room_messages= Message.objects.all()
    return render(request, 'Base/activity.html', {'Room_messages': room_messages})
