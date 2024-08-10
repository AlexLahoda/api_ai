from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    registered = models.DateTimeField(auto_now=True)
    resp_timeout = models.IntegerField(default=10)
    def __str__(self):
        return str(self.id)
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    def __str__(self):
        return 'id: ' + str(self.id) + ' title: ' + self.title

class Comment(models.Model):
    content = models.TextField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    response_text = models.TextField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + "post_id: " + self.post_id.title


