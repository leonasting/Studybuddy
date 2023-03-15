from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User# Importing the models with custom user model

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)# Registering the models with custom user model