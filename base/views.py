from django.shortcuts import render
from django.http import HttpResponse
from .models import Room  # Model we want to query
# Create your views here.



rooms = [
        {"id":1, "name":'Lets Learn Python!'},
        {"id":2, "name":'Design with Me!'},
        {"id":3, "name":'Front End Developers '},
        ]
 

def home(request):
    rooms = Room.objects.all() # Overwrites the earlier defination of rooms
    context = {'rooms' : rooms}
    return render(request,'base/home.html',context) # Passing dictionary key value pair

def room(request,pk):# Pk is acting like query for database query
    room = None
    #for i in rooms:
    #    if i["id"] == int(pk):
    #        room = i
    room = Room.objects.get(id=pk)
    context={'room':room}

    return render(request,'base/room.html',context) 
