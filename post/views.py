from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
# Create your views here.


class post_create_view(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('img', 'post_desc')

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(form)
        return super().form_valid(form)


class post_update_view(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('img', 'post_desc')

    def get_absolute_url(self):
        return reverse('post:create')


class post_delete_view(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('feed:feed')
