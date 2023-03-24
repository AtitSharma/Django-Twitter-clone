from django.db import models
from django.conf import settings
from post.models import Timestap

class Message(Timestap):
    description=models.TextField()
    from_user=models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="sent_message")
    to_user=models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name="received_message")
    
    def __str__(self):
        return str(self.id)
    
    
    
    
    