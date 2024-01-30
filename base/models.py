import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class User_Info(models.Model):
  name = models.CharField(max_length=200)
  chats_id = ArrayField(models.TextField(null=True, blank=True), blank=True)
  friends_id = ArrayField(models.TextField(null=True, blank=True), blank=True)
  
  def __str__(self):
    return str(self.name)
  

class Message(models.Model):
  chat_id = models.IntegerField(primary_key=True)
  chat_users = ArrayField(models.CharField(max_length=50))
  messages = ArrayField(models.TextField(blank=True, null=True), blank=True)
  
  def __str__(self):
    return str(self.chat_id)