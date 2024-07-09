from django.urls import path
from .views import *
from . import views

app_name = 'matrimonyApp'
urlpatterns = [

    path('home/', HomeView.as_view(), name='home'),

    path('parents_details/', parents_details_view, name='parents_details'),
    path('partner_preference/', views.partner_preference_view, name='partner_preference'),

    path('suggestions/',SuggestionView.as_view(), name='suggestions'),

]
