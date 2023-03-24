from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name="User"
        verbose_name_plural="Users"
        
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to="profile",blank=True,null=True)
    contact=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    bio=models.TextField(blank=True,null=True)
    
    
    
    def __str__(self):
        return str(self.user)
    
    