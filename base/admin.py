from django.contrib import admin
from .models import Message, User_Info

# Register your models here.

admin.site.register(Message)
admin.site.register(User_Info)