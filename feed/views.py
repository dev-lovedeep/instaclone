from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from post.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class newsfeed(LoginRequiredMixin, ListView):
    template_name = 'base/news_feed.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'
