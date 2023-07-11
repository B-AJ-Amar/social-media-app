from django.db import models
from users.models import User 
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    # id
    author        = models.ForeignKey(User, on_delete=models.CASCADE)
    title         = models.CharField(blank=True,max_length=255,default="NoTitle")
    content       = models.TextField(blank=True)
    created       = models.DateTimeField(default=timezone.now )
    last_edit     = models.DateTimeField(auto_now=True )
    is_active     = models.BooleanField(blank=True,null=True,default=True)  # not is_archived and author.is_active (curently)
    with_media    = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.author}\n{self.content}"
    
    def get_likes_dislikes(self):
        return [Reaction.objects.filter(post_id=self.id,type='like').count(),
                Reaction.objects.filter(post_id=self.id,type='dislike').count()]
    
    def get_likes(self):
        return Reaction.objects.filter(post_id=self.id,type='like').count()
               

    def get_dislikes(self):
        return  Reaction.objects.filter(post_id=self.id,type='dislike').count()
    
    def user_react(self,user):
        user_react = Reaction.objects.filter(user_id=user,post_id=self)#request.user.
        if user_react.exists():
            return  1 if user_react.first().type == "like" else 2
        return 0



class Reaction(models.Model):
    CHOICES = [
        ('like', 'like'),
        ('dislike', 'dislike'),    
    ]
    # id
    type      = models.CharField(max_length=8, choices=CHOICES,null=True)
    user_id   = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id   = models.ForeignKey(Post, on_delete=models.CASCADE)