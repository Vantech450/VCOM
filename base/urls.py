from django.urls import path
from . import views

urlpatterns = [
  path('register_page/', views.register_page, name="register_page"),
  path('login_page/', views.login_page, name='login_page'),
  path('logout_page/', views.logout_page, name='logout_page'),
  path('search_friends/', views.search_friends, name="search_friends"),
  path('add_friends/', views.add_friends, name='add_friends'),
  path('check_add/', views.check_add, name="check_add"),
  path('check_side_bar/', views.check_side_bar, name="check_side_bar"),
  path('get_messages/', views.get_messages, name="get_messages"),
  path('get_chat/', views.get_chat, name="get_chat"),
  path('refresh_page/', views.refresh_page, name="refresh_page"),
]
