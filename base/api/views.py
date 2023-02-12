#from django.http import JsonResponse  #Initial basic for Json response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = ['GET /api', # Base
            'GET /api/rooms',# All rooms
             'GET /api/rooms/:id']# Specific room
    #return JsonResponse(routes,safe=False)
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms,many=True)#many=True because we are passing multiple objects for querysets
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms,many=False)#\many=False because we are passing single object for query
    return Response(serializer.data)