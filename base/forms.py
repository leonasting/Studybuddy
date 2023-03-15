from django.forms import ModelForm
from .models import Room, User
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # For User Registation

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']
        #exclude = ['password']
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants'] 
          
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','username','email','avatar','bio']
        #exclude = ['password']