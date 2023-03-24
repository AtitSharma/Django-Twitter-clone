from django.shortcuts import render,reverse,get_object_or_404
from django.contrib.auth import get_user_model
from chat.models import Message
from chat.forms import ChatForm
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages

User=get_user_model()

def message_view(request):
    users=User.objects.filter(is_superuser=False)
    context={
        "users":users
    }
    return render(request,"message.html",context)


def message_to_user(request,username):
    users=User.objects.filter(is_superuser=False).exclude(id=request.user.id)
    to_user=User.objects.get(username=username)
    messages=Message.objects.filter(
        from_user__in=[request.user ,to_user]
        ,to_user__in=[request.user ,to_user]).order_by("created_at")
    form=ChatForm(request.POST or None )
    if form.is_valid():
        message=form.save(commit=False)
        message.from_user=request.user
        to_user=User.objects.get(username=username)
        message.to_user=to_user
        message.save()
        return HttpResponseRedirect(reverse("chat:messages_user",args=(username,)))

    context={
        "conversations":messages,
        "form":form,
        "users":users,
        "username":username,
    }
    return render (request,"message.html",context)

class MessageDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Message
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.from_user:
            return True
        return False
    
    def get_success_url(self):
        message=self.get_object()
        messages.add_message(self.request,messages.INFO,"Your message deleted sucessfully")
        username=message.to_user.username
        return reverse("chat:messages_user",args=(username,))
    
    
        
# def delete_message(request):
#     messageid=request.POST.get("messageid")
#     message=get_object_or_404(Message,id=messageid,from_user=request.user)
#     username=message.to_user.username
#     message.delete()
#     messages.add_message(request,messages.INFO,"Your messages deleted sucessfully")
#     return HttpResponseRedirect(reverse("chat:message_user",args=(username,)))





