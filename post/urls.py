from django.urls import path,reverse_lazy
# from django.contrib.auth.views import PasswordChangeView
from post.views import (home,create_post,
                        edit_post,delete_post,
                        like_post,comment_post,
                        PasswordChange)
app_name="post"
urlpatterns=[
    path("",home,name="home"),
    path("create-post/",create_post,name="create_post") ,
    path("edit-post/<int:postid>/",edit_post,name="edit_post"),  
    path('delete-post/',delete_post,name="delete_post"),
    path("like-post/<int:postid>/",like_post,name="like-post"),
    path("comments/<int:postid>/",comment_post,name="comment_post"),
    path("password",PasswordChange.as_view(template_name="password_change_form.html"),
         name="password-change")

]