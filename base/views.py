from django.shortcuts import render
from django.http import HttpResponse
 
# Create your views here.

rooms = [
        {"id":1, "name":'Lets Learn Python!'},
        {"id":2, "name":'Design with Me!'},
        {"id":3, "name":'Front End Developers '},
        ]


def home(request):
    context = {'rooms' : rooms}
    return render(request,'base/home.html',context) # Passing dictionary key value pair

def room(request,pk):# Pk is acting like query for database query
    room = None
    for i in rooms:
        if i["id"] == int(pk):
            room = i
    context={'room':room}

    return render(request,'base/room.html',context) 
