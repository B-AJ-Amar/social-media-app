from django.contrib import admin
from .models import *


# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'gender', 'birthday', 'is_active',"is_admin","is_superuser","is_staff")
    list_filter = ('username', 'email')
    readonly_fields = ('join_date',)
    
    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(Block)
