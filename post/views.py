from django.shortcuts import render,reverse,get_object_or_404,redirect
from post.models import Post,Status,Like
from post.forms import PostForm,CommentForm
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.core.mail import send_mail


def home (request):
    post=Post.objects.filter(status=Status.PUBLIC).order_by("-created_at")
    context={
        "posts":post
    }
    return render(request,'home.html',context)


@login_required()
def create_post(request):
    form=PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.user=request.user      
        obj.save()
        messages.add_message(request,messages.INFO,"Your Post created Sucessfully")
        return HttpResponseRedirect(reverse("post:home"))
        
    context={
        "form":form
    }
    return render(request,"post.html",context)


@login_required()
def edit_post(request,postid):
    # try:
    #     post=Post.objects.get(id=postid)
    # except Post.DoesNotExist:
    #     raise Http404()      
    post=get_object_or_404(Post,id=postid,user=request.user)
    form=PostForm(request.POST or None,instance=post)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.user=request.user  
        obj.save()
        messages.add_message(request,messages.INFO,"Your Post updated Successfully")
        return HttpResponseRedirect(reverse("post:home"))
    return render(request,"post.html",{"form":form})

@login_required
def delete_post(request):
    postid=request.POST.get("postid")
    post=get_object_or_404(Post,id=postid,user=request.user)
    post.delete()
    messages.add_message(request,messages.INFO,"Your post deleted succesfully")
    return HttpResponseRedirect(reverse("post:home"))


@login_required
def like_post(request,postid):
    post=get_object_or_404(Post,id=postid)
    user=request.user
    like,created=Like.objects.get_or_create(post=post,user=user)
    if not created:
        if like.is_liked==True:
            like.is_liked=False
        else:
            like.is_liked=True
        like.save()
    # total=send_mail("Post liked",f"Your post:{post.descrition} has liked","testmyfon321@gmail.com",[user.email])
    
    total_likes=post.likes.filter(is_liked=True).count()
    return JsonResponse({"likes":total_likes},safe=False)

def comment_post(request,postid):
    post=get_object_or_404(Post,id=postid)
    comments=post.comments.all()
    form=CommentForm(request.POST or None)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.user=request.user
        comment.save()
        return HttpResponseRedirect(reverse("post:comment_post",args=(postid,)))


    context={
        "post":post,
        "comments":comments,
        "form":form,
    }

    return render(request,"post_comments.html",context)


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('user:login')
    def get_success_url(self):
        messages.add_message(self.request,messages.INFO,"Your Password Updated Sucessfully now Login with new Password")
        return str(self.success_url)










    
    
    



