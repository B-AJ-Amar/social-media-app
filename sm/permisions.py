from users.models import User,Follow,Block
from posts.models import Post

from django.shortcuts import render,HttpResponse,redirect

def is_owner(request,username):
    try:
        if username!=request.user.username:
            return 0
        else: return 1
    except: return 0
        
def is_blocked(request,username):
    if Block.objects.filter(blocker=request.user,blocked=username).exists() or Block.objects.filter(blocker=username,blocked=request.user).exists(): 
        return 1
    else:return 0 