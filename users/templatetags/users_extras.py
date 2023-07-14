from django import template
from ..models import * 
register = template.Library()







@register.simple_tag
def is_follower(user1,user2):
        return Follow.objects.filter(follower=user1,following=user2).exists()
       