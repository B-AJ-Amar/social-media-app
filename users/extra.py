from django.utils import timezone
import re
from .models import User

def is_birthday_valid(birthday:str):
    user_y = int(str(birthday).split("-")[0])
    curent = timezone.now().year
    
    if ( curent - user_y  < 13) or ( curent - user_y  > 90):
        return "invalid birthday"
    return 0

def is_password_valid(pass1:str,pass2:str):
    if  pass1 !=  pass2:
        return "password not match"
    if len(pass1)<8:
        return "short password"
    return 0

def is_email_valid(mail:str):
    email_pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+' 
     # ! email token
    if User.objects.filter(email=mail).exists():
        return "email token" 
    else:
        # ! email format 
        if  not re.match(email_pattern, mail):
            return "wrong email " 
    return 0
