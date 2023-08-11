from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('about/',about,name="about"),
    path('search/',search,name="search"),
    path('<str:username>/',profile,name="profile"),
    path('<str:username>/followers/',follow,name="followers"),    
    path('<str:username>/following/',follow,name="following"),    
    path('archive/<str:username>/',archive,name="archive"), 
]
