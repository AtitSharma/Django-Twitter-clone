from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from useraccount.models import Profile
from django import forms 
User=get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username","password1","password2")
  
        
class ProfileForms(forms.ModelForm):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.CharField()
    class Meta:
        model=Profile
        fields=["first_name","last_name","email","contact","address","avatar","bio"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]="form-control"


        
class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=["username","email"]
    
        
        
