from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver
from post.models import Post
from django.utils.text import slugify
# Create your models here.


class user_additional_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic', default='profile_pic/avatar.png')
    bio = models.TextField(null=True, blank=True)
    following = models.ManyToManyField(
        User, related_name="following", default=None, blank=True)
    follower = models.ManyToManyField(
        User, related_name="follower", default=None, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = self.user.username
        return super().save(*args, **kwargs)

# automatically delete media when user is deleted
@receiver(post_delete, sender=user_additional_info)
def submission_delete(sender, instance, **kwargs):
    instance.profile_pic.delete(False)
