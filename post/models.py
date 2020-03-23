from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import user_additional_info
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.


class Post(models.Model):
    img = models.ImageField(upload_to="post", blank=True, null=True)
    post_desc = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # def get_absolute_url(self):
    #     return reverse('post:create')

# automatically delete media when post is deleted
@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.img.delete(False)
    # def __str__(self):
    #     return self.author.get_username()
