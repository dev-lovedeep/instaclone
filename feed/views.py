from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from post.models import Post
from user.models import user_additional_info
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class newsfeed(LoginRequiredMixin, ListView):
    template_name = 'base/news_feed.html'
    queryset = Post.objects.all()
    context_object_name = 'posts'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['user'] = user_additional_info.objects.all()
    #     return context
