from django.urls import path
from .views import *
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', user_registration, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),


    path('basic_info/', basic_info_view, name='basic_info'),
    path('lifestyle_info/', lifestyle_view, name='lifestyle_info'),
    path('employment_info/', employment_status_view, name='employment_status'),
    
]