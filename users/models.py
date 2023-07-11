from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
import os

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self , username,email,gender,birthday, password):
        user = self.model(username=username,email=email,birthday=birthday,gender=gender)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self , username,password,email=None,gender=None,birthday=None ):
        user = self.model(username=username,email=email,birthday=birthday,gender=gender)
        user.is_admin         = True
        user.is_staff         = True
        user.is_superuser     = True
        user.verified_badge   = True
        user.set_password(password)
        user.save(using=self._db)
        return user
        



def get_image_upload_path(instance, filename):
    username = instance.username
    return os.path.join('profilephotos', str(username), str(filename))

class User(AbstractBaseUser,PermissionsMixin):
    username             = models.CharField(primary_key=True,max_length=50,blank=True)
    email                = models.EmailField(unique=True,max_length=320,blank=True)
    bio             = models.CharField(max_length=250,default="")
    photo                = models.ImageField(upload_to= get_image_upload_path,default='user_photos/user_default.png')
    join_date            = models.DateTimeField(blank=True,null=True,default=timezone.now)
    birthday             = models.DateField(null=True)
    verified_badge       = models.BooleanField(blank=True,null=True,default=False)
    gender               = models.BooleanField(blank=True,null=True) 
    is_active            = models.BooleanField(blank=True,null=True,default=True)
    is_superuser         = models.BooleanField(blank=True,null=True,default=False)
    is_admin             = models.BooleanField(blank=True,null=True,default=False)
    is_staff             = models.BooleanField(blank=True,null=True,default=False)
    # last_login
    # password 
    
    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS =[  ]
    
    
    def get_followers(self):
        return follow.objects.filter(following=self).count()
    
    def get_followings(self):
        return follow.objects.filter(follower=self).count()





class follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')
    
    def __str__(self) :
        return f"{self.follower}:{self.following}"





