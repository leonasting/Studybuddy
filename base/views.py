from email import message
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q # loop up
from django.http import HttpResponse # Used earlier again added for Restricted Page implementaion 
#from django.contrib.auth.models import User # Importing User for Login
from django.contrib.auth import authenticate, login, logout # Login and logout 
from django.contrib.auth.decorators import login_required# For Restricted Pages
#from django.contrib.auth.forms import UserCreationForm # For User Registation
from .models import Room,Topic, Message, User # Model we want to query
from .forms import RoomForm, UserForm, MyUserCreationForm # Form we want to use

# Create your views here.



rooms = [
        {"id":1, "name":'Lets Learn Python!'},
        {"id":2, "name":'Design with Me!'},
        {"id":3, "name":'Front End Developers '},
        ]
 
def loginPage(request):
    page = "login"# For User Registation segrattion from login
    
    if request.user.is_authenticated: # To safeguard from relogin of user form manual link usage
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get("username").lower()# To convert to lower case
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')
        user = authenticate(request,username=username,password=password) 

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'User does not exist')
             

    context={"page":page}
    return render(request,"base/login_register.html",context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    #page="register"
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)# saving form and saving in time . TO access user right away
            # Reason to clean the data (Capital,rtc)
            user.username = user.username.lower()# To convert to lower case
            user.save()# To save the user
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registation.")

           
    context={"form":form}
    return render(request,"base/login_register.html",context) 



def home(request):
    q = request.GET.get('q')# To retieve the querried parameter
    if not q:
        q=''
    #rooms = Room.objects.all() # Overwrites the earlier defination of rooms
    #rooms = Room.objects.filter(topic__name=q)# __ Query to the Parent
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |#OR
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
        )# __ Query to the Parent

    room_count = rooms.count()# Method to retrieve value based on fiter and its faster than len
    # For Populating topics
    topics = Topic.objects.all()[:5]# To retrieve the topics
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))#all()#.order_by('-created')# To retrieve all the messages for a particular room
    context = {'rooms' : rooms,
               'topics': topics,
               'room_count':room_count,
               'room_messages':room_messages,
               'room_count':room_count,

                }
    return render(request,'base/home.html',context) # Passing dictionary key value pair

def room(request,pk):# Pk is acting like query for database query
    room = None
    #for i in rooms:
    #    if i["id"] == int(pk):
    #        room = i
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')# To retrieve all the messages for a particular room
    participants = room.participants.all()# To retrieve all the participants for a particular room
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)# To add the user to the participants   
        return redirect('room',pk=room.id)# To redirect to the same page and reload after the request

    context={'room':room,'room_messages':room_messages,'participants':participants}

    return render(request,'base/room.html',context) 

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    room_count = Room.objects.all().count()# To retieve the total count for topic component.
    rooms = user.room_set.all()# To retrieve all the rooms for a particular user (children relationship)
    topics = Topic.objects.all()# To retrieve the topics
    room_message = user.message_set.all()# To retrieve all the messages for a particular user (children relationship)
    context={'user':user,
            'rooms':rooms,
            'topics':topics,
            'room_messages':room_message,# For the Feed Component
            'room_count':room_count}
    return render(request,'base/profile.html',context) 





@login_required(login_url='login')
def createRoom(request):
    form = RoomForm() 
    topics = Topic.objects.all()# To retrieve the topics
    if request.method == 'POST':# to Deal with Form submission
        #request.POST.get('name')
        #form = RoomForm(request.POST) Removed in theme installation
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) # topic Object and created boolean
        Room.objects.create(
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            topic = topic,
            host = request.user
        )# To create a room


        """
         if form.is_valid():# Inbuilt methods to check basic validity
            room = form.save(commit=False)# To save the form and get the instance
            room.host = request.user# To link the user to the room
            room.save()
            #form.save()# Backend has been prebuilt
            return redirect('home')# Using url name for redirection 
        """
        return redirect('home')

    context ={'form':form,
              'topics':topics}

    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)# Retrieving a particular object
    topics = Topic.objects.all()# To retrieve the topics
    form = RoomForm(instance = room) # TO link and prefill the form
    if request.user != room.host: # Restrict User who are not the owner
        return HttpResponse("You dont have the permissions!!")

    if request.method == 'POST':# to Deal with Form submission
        #request.POST.get('name')
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) # topic Object and created boolean
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')# Using url name for redirection
        """ form = RoomForm(request.POST,instance=room)# For specific room
        if form.is_valid():# Inbuilt methods to check basic validity
            form.save()# Backend has been prebuilt
            return redirect('home')# Using url name for redirection """

    
    context = {'form':form,
               'topics':topics,
               'room':room}

    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)# Retrieving a particular object

    #form = RoomForm(instance = room) # TO link and prefill the form
    if request.user != room.host: # Restrict User who are not the owner
        return HttpResponse("You dont have the permissions!!")

    if request.method == 'POST':# to Deal with Form submission
        room.delete()# Backend has been prebuilt
        return redirect('home')# Using url name for redirection

    
    context = {'obj':room}

    return render(request,'base/delete.html',context)


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)# Retrieving a particular object
    room_id = message.room.id
    #form = RoomForm(instance = room) # TO link and prefill the form
    if request.user != message.user: # Restrict User who are not the owner
        return HttpResponse("You dont have the permissions!!")

    if request.method == 'POST':# to Deal with Form submission
        message.delete()# Backend has been prebuilt
        return redirect('room',room_id)# Using url name and id for redirection

    
    context = {'obj':message}

    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def updateUser(request):# No Id as User will be the logged in User
    user=request.user
    form = UserForm(instance=user)
    context={'form':form}
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request,'base/update_user.html',context)


def topicsPage(request):
    q = request.GET.get('q')# To retieve the querried parameter
    if not q:
        q=''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)         
        )# __ Query to the Parent
    topics = Topic.objects.filter(name__icontains=q)# To retrieve the topics
    context={'topics':topics,
            'rooms':rooms,
            'q':q}
    return render(request,'base/topics.html',context)

def activityPage(request):
    room_messages = Message.objects.all()#all()#.order_by('-created')# To retrieve all the messages for a particular room
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)