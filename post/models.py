from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import user_additional_info

# Create your models here.


class Post(models.Model):
    img = models.ImageField(upload_to="post", blank=True, null=True)
    post_desc = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('post:create')

    # def __str__(self):
    #     return self.author.get_username()
