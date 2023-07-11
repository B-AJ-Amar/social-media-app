from django import template
from ..models import * 
register = template.Library()




@register.simple_tag
def user_react(post,user):
        user_react = Reaction.objects.filter(user_id=user,post_id=post)#request.user.
        if user_react.exists():
            return  1 if user_react.first().type == "like" else 2
        return 0