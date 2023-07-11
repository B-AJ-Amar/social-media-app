from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login,name="login"),
    path('signup/',signup,name="signup"),
    path('logout/',logout,name="logout"),
    path('un_follow/<str:username>',un_follow,name="un_follow"),
    path('reset_password/<str:username>',reset_password,name="reset_password"),
    path('delete/<str:username>',delete,name="delete_account"),
]
