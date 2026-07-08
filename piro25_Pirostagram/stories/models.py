from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}의 스토리'