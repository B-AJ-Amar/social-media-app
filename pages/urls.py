from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('about/',about,name="about"),
    path('search/',search,name="search"),
    path('profile/<str:username>/',profile,name="profile"),   
    path('archive/<str:username>/',archive,name="archive"),  
]
