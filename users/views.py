from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout ,get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import re
from .models import *
from posts.models import *

User = get_user_model()

# Create your views here.


# ? =====================================================================================
# ? AUTH FUNCTIONS ======================================================================
# ? =====================================================================================

# ? SIGNUP : ---------------------------------------------------------------------

def login(request):
    # cant go to login again
    if request.user.is_authenticated:
        return redirect("/") 
    
    
    if request.method == 'POST' :
        Ausername = request.POST.get('username')
        Apassword = request.POST.get('password')

            
        user = authenticate(request, username=Ausername, password=Apassword)
        if user is not None:
            if  "remember" not in request.POST:
                request.session.set_expiry(0)
            auth_login(request, user)
            return redirect("/") 
        else:
            messages.info(request,f'Invalid username or password {user}') 
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')
    
    

# ? LOGOUT : ---------------------------------------------------------------------
def logout(request):
    
    if  request.user.is_authenticated:
        auth_logout(request)
    return redirect("/accounts/login") 

   






# ? SIGNUP : ---------------------------------------------------------------------


def signup(request):
    # TODO : password seq, age
    
    # cant go to login again
    if request.user.is_authenticated:
        return redirect("/") 
    
    if request.method == "POST" and "signupbtn" in  request.POST  :

        email_pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+' 
        
        t_username    = None
        t_email       = None
        t_password    = None
        t_re_password = None
        t_birthday    = None
        t_gender      = None
           
        # check if vvrs exist 
        if "username" in request.POST :
            t_username =request.POST["username"]
            
        if  "password" in request.POST:
            t_password =request.POST["password"]
            
        if  "re_password" in request.POST:
            t_re_password =request.POST["re_password"]
            
        if  "email" in request.POST :
            t_email = request.POST["email"]
        
        if  "gender" in request.POST :
            t_birthday = request.POST["birthday"]
        
        if  "gender" in request.POST :
            t_gender = request.POST["gender"]
            
        if t_username and t_password and t_re_password and t_email and t_birthday and t_gender : 
            # ! username token
            if  User.objects.filter(username=t_username).exists():
                messages.error(request,"username token")    
            else :
                # ! email token
                if User.objects.filter(email=t_email).exists():
                    messages.error(request,"email token") 
                else:
                    # ! email format 
                    if  not re.match(email_pattern, t_email):
                        messages.error(request,"wrong email ") 
                    else :
                        # ! same password
                        if  t_password !=  t_re_password:
                            messages.error(request,"password not match")          
                        else :
                            # ! short password
                            if len(t_password)<8:
                                messages.error(request,"short password")
                            else :
                                if timezone.now().year - int(str(t_birthday).split("-")[0]) < 13:
                                    messages.warning(request," age")
                                else:
                                    
                                    user = User.objects.create_user(
                                        username=t_username,
                                        email=t_email,
                                        birthday=t_birthday,
                                        password=t_password,
                                        gender= True if t_gender=="male" else False
                                        )
                                
                                    messages.success(request,"added successesfuly")  
                                    return redirect("login")  
                                            
        else:
            messages.error(request,f"empty feilds")
        messages.error(request,f"empty feilds, {request.POST} ")
        context = {"name":t_username,
                   "email":t_email,
                   "pass1":t_password,
                   "pass2":t_re_password,
                   "birthday":t_birthday
                   }
        return render(request,"users/signup.html",context)
        
    else :
        return render(request,"users/signup.html")


# ? follow ======================================================


@login_required(login_url="/accounts/login/")
def un_follow(request,username,*args):
    if request.method == "POST" and ( ("un_followbtn"  in request.POST) or( "un_follow_sr_btn" in request.POST))  :
        if follow.objects.filter(follower=request.user,following=username).exists():
            follow.objects.filter(follower=request.user,following=username).delete()
        else :
            follow.objects.create(follower=request.user,following= User.objects.get(username=username))
    
        return redirect(f"/profile/{username}")
    return render(request,"nav.html")
    
    
    
    
@login_required(login_url="/accounts/login/")
def reset_password(request,username):
    if request.user.username != username:
        return redirect("/")
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect(f"/profile/{request.user.username}")
    if request.method == "POST" and "resetpasswordbtn" in request.POST:
        
        new_password1 = request.POST["new_password1"] if "new_password1" in request.POST else ""
    
        new_password2 = request.POST["new_password2"] if "new_password2" in request.POST else ""
    
        old_password  = request.POST["old_password"]  if "old_password"  in request.POST else ""
            
        user = authenticate(request,username=request.user.username,password=old_password)
        if user is not None:
             # ! same password
            if  new_password1 !=  new_password2:
                messages.error(request,"password not match")          
            else :
                # ! short password
                if len(new_password1)<8:
                    messages.error(request,"short password")
                else:
                    user.set_password(new_password1)
                    user.save()
                    return redirect("/")
        else : 
            messages.error(request,"wrong password")
    return render(request,"users/reset_password.html")







@login_required(login_url="/accounts/login/")
def delete(request,username):
    if request.user.username != username:
        return redirect("/")
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect(f"/profile/{request.user.username}")
     
    if request.method == "POST" and "deleteaccountbtn" in request.POST:
        
        
        
        User.objects.get(username=username).is_active = False
        
        # desactivate all posts
        up = Post.objects.filter(author=username)
        for p in up:
            p.is_active = False
            p.save()
            
        ur = Reaction.objects.filter(user_id=username)
        
        # delete all reactions 
        for r in ur:
            r.delete()
           
        
        
    
        return redirect(f"/profile/{username}")
    