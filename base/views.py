import json
import ast
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import User_Info, Message

# Create your views here.

@csrf_exempt
def login_page(request):
  
  if request.method == 'POST':
    received_data = json.loads(request.body.decode('utf-8'))
    username = received_data.get('username', '')
    password = received_data.get('password', '')
    
    try:
      user = authenticate(request, username=username, password=password)
    except:
      messages.error('Error while trying to login')
      
    if user != None:
      login(request, user)
      
      send_data = {
        'message': 'Successfully login',
      }
      return JsonResponse(send_data)
    else:
      messages.error('User does not exist')


@csrf_exempt
def register_page(request):
  if request.method == 'POST':
    received_data = json.loads(request.body.decode('utf-8'))
    form = UserCreationForm(received_data)
        
    if form.is_valid():
      form.save()
      
      username = received_data.get('username', '')
      password = received_data.get('password1', '')
      
      user = authenticate(request, username=username, password=password)
      
      login(request, user)
      
      User_Info.objects.create(
        name = request.user.username,
        chats_id = [],
        friends_id = [],
      )
      
      add_current_user_id = User_Info.objects.get(name=request.user.username)
      add_current_user_id.friends_id.append(request.user.id)
      add_current_user_id.save()
      
      send_data = {
        'message': 'Account successfully created',
      }
      return JsonResponse(send_data)
    else:
      return JsonResponse({'errors': form.errors}, status=400)



@csrf_exempt
def logout_page(request):
  
  if request.method == 'POST':
  
    logout(request)
    send_data = {
      'message': 'Logout Success'
    } 
    return JsonResponse(send_data)
  

@csrf_exempt
def search_friends(request):
  
  if request.method == 'POST':
    received_data = json.loads(request.body.decode('utf-8'))
    get_data = received_data.get('search_input', '')
  
    try:
      check_users = User.objects.filter(Q(username__icontains=get_data))
    except:
      messages.error('User does not exist')

    if check_users != None:
      users_id = []
      users = []
      for user in check_users:
        users.append(str(f'{user}'))
        get_user_id = User.objects.get(username=user)
        users_id.append(get_user_id.id)
          
      send_data = {
        'users': users,
        'users_id': users_id,
      }
      return JsonResponse(send_data)
    else:
      messages.error('User does not exist')
      
  
@csrf_exempt
def add_friends(request):
  
  if request.method == 'POST':
    received_data = json.loads(request.body.decode('utf-8'))
    get_data = received_data.get('user', '')
    
    user = User.objects.get(username=get_data)
    user_id = user.id
    
    use_id = f'{request.user.id}{user_id}'
    
    Message.objects.create(
      chat_id = int(use_id),
      chat_users = [request.user.username, get_data],
      messages = [],
    )
    
    current_user = User_Info.objects.get(name=request.user.username)
    current_user.chats_id.append(int(use_id))
    current_user.friends_id.append(user_id)
    current_user.save()
    
    other_user = User_Info.objects.get(name=get_data)
    other_user.chats_id.append(int(use_id))
    other_user.friends_id.append(request.user.id)
    other_user.save()
    
    check_add_button = current_user.friends_id
    get_messages = current_user.chats_id
    
    send_data = {
      'message': 'Added Friends Success',
      'check_add_button': check_add_button,
      'get_messages': get_messages,
    }
    return JsonResponse(send_data)


@csrf_exempt
def check_add(request):
  if request.method == 'GET':
    
    user = User_Info.objects.get(name=request.user.username)
    messages_room = user.chats_id
    check_add_button = user.friends_id
  
    send_data = {
      'messages_room': messages_room,
      'check_add_button': check_add_button,
    }
    return JsonResponse(send_data)
  

@csrf_exempt
def check_side_bar(request):
  
  if request.method == 'GET':
    
    user = User_Info.objects.get(name=request.user.username)
    room_messages = user.chats_id
    room_messages = [int(room_id) for room_id in room_messages]
    side_bar = []
    side_bar_user = []
    
    
    for room in room_messages:
      available_users = Message.objects.get(chat_id=room)
      friend = available_users.chat_users
      friend = [username for username in friend if username != f'{request.user.username}']
      show_friend = friend.pop()
      side_bar_user.append(show_friend)
      
      side_bar_update = available_users.messages
      
      if side_bar_update != []:
        side_bar_user.append(ast.literal_eval(side_bar_update.pop()))
      else:
        side_bar_user.append('')
      
      side_bar_user.append(room)
      
      side_bar.append(side_bar_user)
      
      side_bar_user = []
    
    
    get_messages = Message.objects.get(chat_id=room_messages[0])
    display_messages = []
    
    get_the_messages = get_messages.messages
    
    
    for message in get_the_messages:
      unarray_this = ast.literal_eval(message)
      display_messages.append(unarray_this)
    
    
    send_data = {
      'user': request.user.username,
      'side_bar': side_bar,
      'display_messages': display_messages,
      'current_chat_id': room_messages[0],
      'room_messages': room_messages,
    }
  
    return JsonResponse(send_data)
  
  
@csrf_exempt
def get_messages(request):
  
  if request.method == 'POST':
    
    received_data = json.loads(request.body.decode('utf-8'))
    get_message = received_data.get('message', '')
    get_chat_id = int(received_data.get('chat_id', ''))
    get_user = received_data.get('user', '')
    
    create_array = []
    create_array.append(get_user)
    create_array.append(get_message)
    
    
    store_message = Message.objects.get(chat_id=get_chat_id)
    store_message.messages.append(create_array)
    store_message.save()
    
    create_array = []
    
    get_user = User_Info.objects.get(name=request.user.username)
    message_id = get_user.chats_id
    message_id.remove(str(get_chat_id))
    message_id.insert(0, get_chat_id)
    get_user.save()
    
    send_data = {
      'message': 'Success',
    }
  
    return JsonResponse(send_data)
  
  
@csrf_exempt
def get_chat(request):
  if request.method == 'POST':
    
    received_data = json.loads(request.body.decode('utf-8'))
    get_data = int(received_data.get('user', ''))
    
    user = Message.objects.get(chat_id=get_data)
    chats = user.messages
    
    send_data = {
      'chats': chats,
      'chat_id': get_data,
    }
    
    return JsonResponse(send_data)
  
  
@csrf_exempt
def refresh_page(request):
  
  if request.method == 'GET':
    
    user = User_Info.objects.get(name=request.user.username)
    updated_chat_id = user.chats_id
  
    send_data = {
      'updated_chat_id': updated_chat_id
    }
    
    return JsonResponse(send_data)