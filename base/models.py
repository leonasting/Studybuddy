from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self): # String Representation
        return self.name

class Room(models.Model):
    host =  models.ForeignKey(User,on_delete = models.SET_NULL,null=True)  
    topic = models.ForeignKey(Topic,on_delete = models.SET_NULL,null=True)# allowing empty values in DB
    name = models.CharField(max_length=200)
    description = models.TextField(null = True,blank = True) # Null is for databse having empty, blacnk is for form field
    participants = models.ManyToManyField(User,related_name="participants",blank=True) # If you comment on something
    updated = models.DateTimeField(auto_now=True) # Latest Interaction captured
    created = models.DateTimeField(auto_now_add=True) # First Interaction captured

    class Meta:
        ordering = ['-updated','-created'] # Negative for inverse ordering
    def __str__(self): # String Representation
        return self.name


class Message(models.Model):# Many to 1 with Room
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    room = models.ForeignKey(Room,on_delete = models.CASCADE)# if ROOM is deleted message is also deleted
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True) # Latest Interaction captured
    created = models.DateTimeField(auto_now_add=True) # First Interaction captured

    def __str__(self): # TO represent only the first 50 characters
        return self.body[:50]


