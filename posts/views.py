from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.utils import timezone
# Create your views here.


@login_required(login_url="/accounts/login/")
def create(request):
    context = {
             "title":"",
             "content":""
            
        }
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect("/")
        
    if request.method == "POST" and "createbtn" in request.POST:
        if "title" in request.POST:
            context["title"] = str(request.POST["title"]).strip()
        if "content" in request.POST:
            context["content"] = str(request.POST["content"]).strip()
          
        if len(context["title"])>=255:
            messages.error(request,"too long title")
        else:
            if not len(context["content"]):
                messages.error(request,"content is empty")
            else:
                if not len(context["title"]):
                    context["title"]="NoTitle"
                Post.objects.create(author=request.user,title=context["title"],content=context["content"])
                
                messages.success(request,"post created successfully")
                # HttpResponse("done")
                return redirect(f"/profile/{request.user.username}")    
       
    return render(request,"posts/create.html",context)



@login_required(login_url="/accounts/login/")
def edit(request,post_id):
    
    try:
        p = Post.objects.get(id=post_id)
    except:
        return redirect("/")
    context = {
             "title":"",
             "content":""
            
        }
    if p.author != request.user:
        return redirect("/")
        
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect("/")
        
    if request.method == "POST" and "editbtn" in request.POST:
        if "title" in request.POST:
            context["title"] = str(request.POST["title"]).strip()
        if "content" in request.POST:
            context["content"] = str(request.POST["content"]).strip()
          
        if len(context["title"])>=255:
            messages.error(request,"too long title")
        else:
            if not len(context["content"]):
                context["content"] = p.content
            
            if not len(context["title"]):
                context["title"]=p.title
                
            p.title = context["title"]
            p.content = context["content"]
            p.last_edit = timezone.now()
            p.save()
                # Post.objects.create(author=request.user,title=context["title"],content=context["content"])
                
            messages.success(request,"post edited successfully")
                # HttpResponse("done")
            return redirect(f"/profile/{request.user.username}")    
       
    return render(request,"posts/edit.html",{"post":p})






@login_required(login_url="/accounts/login/")
def delete(request,post_id):
    try:
        p = Post.objects.get(id=post_id)
    except:
        return redirect("/")
        
   
    if p.author != request.user:
        return redirect("/")
        
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect("/")
        
    if request.method == "POST" and "deletebtn" in request.POST:
        
        p.delete()
                
        messages.success(request,"post deleted successfully")
            # HttpResponse("done")
        return redirect(f"/profile/{request.user.username}")    
    
    return render(request,"posts/delete.html",context = {"post":p })




@login_required(login_url="/accounts/login/")
def addtoarchive(request,post_id):
    try:
        p = Post.objects.get(id=post_id)
    except:
        return redirect("/")
        
   
    if p.author != request.user:
        return redirect("/")
        
    if request.method == "POST" and "cancelbtn" in request.POST:
         return redirect("/")
        
    if request.method == "POST" and "archivebtn" in request.POST:
        
        p.is_active = False if p.is_active else True
        p.save()
                
        messages.success(request,"post added to Archive successfully")
            # HttpResponse("done")
    return redirect(f"/archive/{p.author.username}/")     
    




@login_required(login_url="/accounts/login/")
def post(request,post_id):
    
    try:
        p = Post.objects.get(id=post_id)
    except:
        return redirect("/")
    
    # if the post exists
    if not p.author.is_active or not p.is_active:
        return redirect("/")
    
    context = {
        "post" :  p,
    }                   
    return render(request,"posts/post.html",context)



# ! AJAX ===============================================

@login_required(login_url="/accounts/login/")
def react(request,post_id:int):
    # 0 
    # 1 delete like
    # 2 to     like
    # 3 make   like
    # 4 delete dislike
    # 5 to     dislike
    # 6 make   dislike
    type = request.POST.get("type")
    print(f"type =========================== {request.POST}")
    if not type: return JsonResponse({"msg":"bad request"},safe=False,status=400)  #bad request
    if type == "likebtn":
        reaction = Reaction.objects.filter(user_id=request.user,post_id=Post.objects.get(id=post_id))
        if reaction.exists():
            reaction = reaction.first()
            if reaction.type == "like":
                reaction.delete()
                return JsonResponse({"msg":1},safe=False, status=200) 
                
            else:
                reaction.type = "like"
                reaction.save()
                return JsonResponse({"msg":2},safe=False, status=200) 
        else:
            Reaction.objects.create(type="like",user_id=request.user,post_id=Post.objects.get(id=post_id))
            return JsonResponse({"msg":3},safe=False, status=200) 
    
    elif  type == "dislikebtn":
        reaction = Reaction.objects.filter(user_id=request.user,post_id=Post.objects.get(id=post_id))
        if reaction.exists():
            reaction = reaction.first()
            if reaction.type == "dislike":
                reaction.delete()
                return JsonResponse({"msg":1},safe=False, status=200) 
            else:
                reaction.type = "dislike"
                reaction.save()
                return JsonResponse({"msg":5},safe=False, status=200) 
        else:
            Reaction.objects.create(type="dislike",user_id=request.user,post_id=Post.objects.get(id=post_id))
            return JsonResponse({"msg":3},safe=False, status=200) 

