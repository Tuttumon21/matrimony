from django.urls import path
from .views import *
from . import views

app_name = 'matrimonyApp'
urlpatterns = [

    path('home/', HomeView.as_view(), name='home'),

    path('parents_details/', parents_details_view, name='parents_details'),
    path('partner_preference/', views.partner_preference_view, name='partner_preference'),

    path('suggestions/',SuggestionView.as_view(), name='suggestions'),

    path('exclude_profile/<int:profile_id>/', ExcludeProfileView.as_view(), name='exclude_profile'),


    path('send_request/<int:profile_id>/', views.send_request, name='send_request'),
    
    path('respond_to_request/<int:request_id>/<str:action>/', views.respond_to_request, name='respond_to_request'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),
    path('friends_list/', FriendsListView.as_view(), name='friends_list'),

 path('send_message/<int:recipient_id>/', send_message, name='send_message'),
    path('chat/<int:friend_id>/', chat_room, name='chat_room'),
    
    path('chat/', views.chat_with_friends, name='chat_with_friends'),
    path('chat/<str:room_name>/', views.chat_with_friends, name='chat_with_friends'),
]
