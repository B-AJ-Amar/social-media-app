from django.shortcuts import render,HttpResponse,redirect
from users.models import User,Follow,Block
from posts.models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/accounts/login/")
def home(request):
 
    # get all followed by user
    following = list(set(Follow.objects.filter(follower=request.user).values_list('following', flat=True)))
    
    following.append(request.user.username)
    # get eny post created by the privious users (following)
     # list(set(following)) in this part ,set() to remove duplicated values
    posts = Post.objects.filter(is_active=True,author__in=following).exclude(author__in= list(Block.objects.filter(blocker=request.user).values_list('blocked', flat=True)))
    
    return render(request,"pages/home.html",{
                                                "posts":posts.order_by("-last_edit"),
                                                })

def about(request):
    return render(request,"pages/about.html")



@login_required(login_url="/accounts/login/")
def profile(request,username):
    
    if Block.objects.filter(blocker=request.user,blocked=username).exists() or Block.objects.filter(blocker=username,blocked=request.user).exists(): 
        return redirect(f"/accounts/blocked_list/{request.user.username}")
    user = User.objects.get(username=username)
    if user != request.user and user.is_privite  and not Follow.objects.filter(follower=request.user,following=user).exists():
         posts = None
    else:
        posts =  Post.objects.filter(author=user,is_active=True).order_by("-created")
    context = {"user_page" : user,
               "posts"     : posts,
               "follow"    : False,
               
               }
    if user != request.user:
        if Follow.objects.filter(follower=request.user,following=user).exists():
            context[ "follow" ] = True
    # return HttpResponse(f"{context['follow']}")
    return render(request,"pages/profile.html",context)


@login_required(login_url="/accounts/login/")
def archive(request,username):
     return render(request,"pages/archive.html",context = {"posts":Post.objects.filter(author=username,is_active=False).order_by("-created") })
    
   

@login_required(login_url="/accounts/login/")
def search(request):
    # user = request.user
    if request.method == "GET" and "searchbtn" in request.GET:
        if 'searchbar' in request.GET:
            result = request.GET['searchbar']
            
        exc = list(Block.objects.filter(blocker=request.user).values_list('blocked', flat=True))
        results = {
            "sr_users"    :  User.objects.filter(username__icontains=result,is_active=True).exclude(username__in= exc ),
            "sr_posts"    :  Post.objects.filter(content__icontains=result,is_active=True).exclude(author__in= exc),
            "search"      : result
        }
        # return HttpResponse(f"{results['sr_posts']}")
        
        return render(request,"pages/search.html",results)
    




