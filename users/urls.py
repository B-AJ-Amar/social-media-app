from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login,name="login"),
    path('signup/',signup,name="signup"),
    path('logout/',logout,name="logout"),
    path('un_follow/<str:username>',un_follow,name="un_follow"),
    path('requests/<str:username>/',requests,name="requests"), 
    path('requests/respnse/<str:username>/',requests_response,name="requests_response"),
    path('privite_public/<str:username>',privite_public,name="privite_public"),
    path('reset_password/<str:username>',reset_password,name="reset_password"),
    path('delete/<str:username>',delete,name="delete_account"),
]
