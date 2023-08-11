from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout ,get_user_model
from django.contrib.auth.decorators import login_required
from .extra import *

from .models import *
from posts.models import *
from sm.permisions import *

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
        if user is not None and user.is_active:
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
        
        t_username    = request.POST.get("username", None)
        t_email       = request.POST.get("email", None)
        t_password    = request.POST.get("password", None)
        t_re_password = request.POST.get("re_password", None)
        t_birthday    = request.POST.get("birthday", None)
        t_gender      = request.POST.get("gender", None)
           
        
        if t_username and t_password and t_re_password and t_email and t_birthday and t_gender : 
            # ! username token
            if  User.objects.filter(username=t_username).exists():
                messages.error(request,"username token")    
            else :
                # ! email 
                if is_email_valid(t_email):
                    messages.error(request,"email token") 
                else:
                    # !  password
                    is_pass_valid = is_password_valid(t_password,t_re_password) 
                    if is_pass_valid :
                        messages.error(request,"wrong email ") 
                    else :
                        if  is_birthday_valid(t_birthday) :
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
                            # Follow.objects.create(follower=user,following="amar") 
                            return redirect("login")  
                                        
        else:
            messages.error(request,f"empty feilds")
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
def reset_password(request,username):
    if not is_owner(request,username):
        return render(request,"404.html")
    
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
    if not is_owner(request,username):
        return render(request,"404.html")
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect(f"/profile/{request.user.username}")
     
    if request.method == "POST" and "deleteaccountbtn" in request.POST:
        cn = request.POST.get("confirminput",None)
        if cn == request.user.username :
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
        
            auth_logout(request)
            return redirect("/accounts/login") 
        else:
            messages.error(request,"something went wrong")
            return render(request,"users/delete_account.html")
            
    if  request.method == "GET":
        return render(request,"users/delete_account.html")
         
    

@login_required(login_url="/accounts/login/")
def privite_public(request,username):
    if not is_owner(request,username):
        return render(request,"404.html")
    
    user = User.objects.get(username=username)
    if request.method == "GET":
        return render(request,"users/privite_public.html",context={"user_page":user})
        
    if request.method == "POST" and "confirmbtn" in request.POST:
        if not user.is_privite:
            user.is_privite = True
        else:
            if FollowrRquests.objects.filter(reciver=request.user).exists():
                messages.warning(request,"Your account cannot be made public until you have responded to all the follow requests.")
                return render(request,"users/privite_public.html",context={"user_page":user})
            else:
                user.is_privite = False
        user.save()
    return redirect(f"/profile/{username}")
    
    
#! AJAX  =================================

@login_required(login_url="/accounts/login/")
def follow(request):
    # 0 : error
    # 1 : followed
    # 2 : unfollowed
    # 3 : requested
    # 4 : request-canceld
    
    if request.method == "POST" :
        username = request.POST.get("username")
        try:
            user =  User.objects.get(username=username)
        
            
            fr = Follow.objects.filter(follower=request.user,following=user)
            if fr.exists():
                fr.delete()
                return JsonResponse({"msg":2},safe=False, status=200)
            else :   
                if user.is_privite:
                    fr = FollowrRquests.objects.filter(sender=request.user,reciver=user)
                    if fr.exists():
                        fr.delete()
                        return JsonResponse({"msg":4},safe=False, status=200)
                    else:
                        FollowrRquests.objects.create(sender=request.user,reciver=user)
                        return JsonResponse({"msg":3},safe=False, status=200)
                else:
                    Follow.objects.create(follower=request.user,following=user)
                    return JsonResponse({"msg":1},safe=False, status=200)
        except:
            return JsonResponse({"msg":0})
       
    return JsonResponse(status=404)



    
@login_required(login_url="/accounts/login/")
def requests(request,username,*args):
    if  request.method == "GET"  : 
        rq_users = list(FollowrRquests.objects.filter(reciver=request.user).values_list('sender', flat=True))
        rq_users = User.objects.filter(is_active=True,username__in=rq_users)
        return render(request,"pages/requests.html",{"rq_users":rq_users}) 
    
    if request.method == "POST":    
        btn = request.POST.get("btn")
        username = request.POST.get("username")
        user =  User.objects.get(username=username) 
        if  btn == "confirm_btn"  :
            Follow.objects.create(follower=user,following=request.user)
            FollowrRquests.objects.filter(sender=user,reciver=request.user).delete()
            return JsonResponse({"msg":1})
        elif  btn == "ignore_btn" :
            FollowrRquests.objects.filter(sender=user,reciver=request.user).delete()
            return JsonResponse({"msg":2})
        return JsonResponse({"msg":0})
    


@login_required(login_url="/accounts/login/")
def blocked_list(request):
    if  request.method == "GET"  : 
        bc_users = list(Block.objects.filter(blocker=request.user).values_list('blocked', flat=True))
        bc_users = User.objects.filter(is_active=True,username__in=bc_users)
        return render(request,"pages/blocked_list.html",{"blocked_list":bc_users}) 
    
    if  request.method == "POST"  :
        btn = request.POST.get("btn")
        username = request.POST.get("username")
        try: 
            user =  User.objects.get(username=username) 
        except:
            return JsonResponse({"msg":0},status=404)
        if btn == "unblock_btn":
            Block.objects.filter(blocker=request.user,blocked=user).delete()
            return JsonResponse({"msg":1})
        elif "block_btn" in  request.POST  :
            try :
                Follow.objects.get(follower=request.user,following=user).delete()
            except: pass
            try :
                Follow.objects.get(follower=user,following=request.user).delete()
            except: pass
            try :
                FollowrRquests.objects.filter(sender=request.user,reciver=user).delete()
            except: pass
            try :
                FollowrRquests.objects.filter(sender=user,reciver=request.user).delete()
            except: pass
            Block.objects.create(blocker=request.user,blocked=user)
            print("blocked")
            return redirect("/accounts/blocked_list/")
            # print("donne")
        return JsonResponse({"msg":0})
    