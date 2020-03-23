from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.

# for user creation we are using default USER model

# to implement following and follower


# class User(models.Model):
#     def get_absolute_url(self):
#         return reverse('user:login', kwargs={})


class user_additional_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic', default='avatar.png')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# automatically delete media when user is deleted
@receiver(post_delete, sender=user_additional_info)
def submission_delete(sender, instance, **kwargs):
    instance.profile_pic.delete(False)


class follow(models.Model):
    following = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse('user:newuser', kwargs={})
