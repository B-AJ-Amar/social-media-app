from django.urls import path,include,reverse
from .views import *
# url = reverse('posts:react',id)
urlpatterns = [
    
    path('create/',create,name="create_post"),
    path('addtoarchive/<int:post_id>/',addtoarchive,name="archive_post"),
    path('delete/<int:post_id>/',delete,name="delete_post"),
    path('edit/<int:post_id>/',edit,name="edit_post"),
    path('react/<int:post_id>/',react,name="react"),
    path('post/<int:post_id>/',post,name="post"),
    
]
