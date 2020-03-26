from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from post.models import Post
from user.models import user_additional_info
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import random

# Create your views here.


class newsfeed(LoginRequiredMixin, ListView):
    template_name = 'base/news_feed.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        logged_in_user = get_object_or_404(
            user_additional_info, user=self.request.user)
        context['logged_in_user_following_list'] = logged_in_user.following.all()
        context['logged_in_user_follower_list'] = logged_in_user.follower.all()
        # this is super awesome #select random rows from model
        context['all_users'] = user_additional_info.objects.order_by('?')[:5]
        print(user_additional_info.objects.all())
        return context
