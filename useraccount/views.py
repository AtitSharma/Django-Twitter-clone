from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from useraccount.forms import ProfileForms,UserUpdateForm,SignUpForm
from django.urls import reverse_lazy
from useraccount.models import Profile
from django.contrib.auth.decorators import login_required
User=get_user_model()



def user_login(request):
    form=AuthenticationForm(request.POST or None)
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse("post:home"))
        else:
            messages.add_message(request,messages.ERROR,"Invalid username or password")
    return render(request,"login.html",{"form":form})


# This is the replace of user_login function 
class UserLoginview(LoginView):
    template_name="login.html"

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("user:login"))




class SignupView(CreateView):
    template_name="login.html"
    form_class=SignUpForm
    model=User
    success_url=reverse_lazy("user:login")
    
    
    def form_valid(self, form):
        user=form.save()
        Profile.objects.create(user=user)
        return super().form_valid(form)
    
    

def profile_view(request,username):
    user=get_object_or_404(User,username=username)
    form=None
    if request.user.is_authenticated and request.user.username==username:
        user=request.user
        initial_data={"first_name":user.first_name,"last_name":user.last_name,"email":user.email}
        form=ProfileForms(request.POST or None, request.FILES or None, instance=request.user.profile,initial=initial_data)
        if form.is_valid():
            user.save()
            form.save()
    return render(request,'profile.html',{"user":user,"form":form})

@login_required
def profile_update_view(request):
    user=request.user
    initial_data={"first_name":user.first_name,"last_name":user.last_name,"email":user.email}
    form=ProfileForms(request.POST or None,instance=request.user.profile,initial=initial_data)
    if form.is_valid():
        user=request.user
        user.first_name=form.cleaned_data.get("first_name")
        user.last_name=form.cleaned_data.get("last_name")
        user.email=form.cleaned_data.get("email")
        user.save()
        form.save()
        messages.add_message(request,messages.SUCCESS,f"Your post updated sucessfully")
        return HttpResponseRedirect(reverse("user:profile",args=(request.user.username,)))
    
    return render(request,"profile.html",{"form":form})
        
        
    


    
    


