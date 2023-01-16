from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic # Model we want to query
from .forms import RoomForm
# Create your views here.



rooms = [
        {"id":1, "name":'Lets Learn Python!'},
        {"id":2, "name":'Design with Me!'},
        {"id":3, "name":'Front End Developers '},
        ]
 

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
    topics = Topic.objects.all()# To retrieve the topics

    context = {'rooms' : rooms,
               'topics': topics,
               'room_count':room_count,
                }
    return render(request,'base/home.html',context) # Passing dictionary key value pair

def room(request,pk):# Pk is acting like query for database query
    room = None
    #for i in rooms:
    #    if i["id"] == int(pk):
    #        room = i
    room = Room.objects.get(id=pk)
    context={'room':room}

    return render(request,'base/room.html',context) 

def createRoom(request):
    form = RoomForm() 
    if request.method == 'POST':# to Deal with Form submission
        #request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():# Inbuilt methods to check basic validity
            form.save()# Backend has been prebuilt
            return redirect('home')# Using url name for redirection

    context ={'form':form}

    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)# Retrieving a particular object

    form = RoomForm(instance = room) # TO link and prefill the form
    if request.method == 'POST':# to Deal with Form submission
        #request.POST.get('name')
        form = RoomForm(request.POST,instance=room)# For specific room
        if form.is_valid():# Inbuilt methods to check basic validity
            form.save()# Backend has been prebuilt
            return redirect('home')# Using url name for redirection

    
    context = {'form':form}

    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)# Retrieving a particular object

    #form = RoomForm(instance = room) # TO link and prefill the form
    if request.method == 'POST':# to Deal with Form submission
        room.delete()# Backend has been prebuilt
        return redirect('home ')# Using url name for redirection

    
    context = {'obj':room}

    return render(request,'base/delete.html',context)