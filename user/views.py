from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
# Create your views here.


def usersignup(request):
    if request.method == "POST":
        user_data = user_signup_form(data=request.POST)
        user_additional_data = user_additional_info_form(data=request.POST)

        if user_data.is_valid() and user_additional_data.is_valid():
            user = user_data.save()
            user.set_password(user.password)
            user.save()

            additional_data = user_additional_data.save(commit=False)
            additional_data.user = user
            if 'profile_pic' in request.FILES:
                additional_data.profile_pic = request.FILES['profile_pic']
            additional_data.save()
            return HttpResponseRedirect(reverse('user:login'))
        return HttpResponse("form is getting invalid")

    else:

        return render(request, 'user/signup.html', {
            "user_basic": user_signup_form(),
            "user_additional": user_additional_info_form()
        })


def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # print(get_user_model().objects.filter(
        #     username=username).values("username")[0]["username"])

        if user:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url and next_url != '/':
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse('feed:feed'))
        else:
            if not get_user_model().objects.filter(username=username):
                return HttpResponse("no accout with username {} exist".format(username))
            else:
                return HttpResponse("invalid credentials")
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('feed:feed'))
        else:
            return render(request, "user/login.html", {})


class userprofile(LoginRequiredMixin, generic.DetailView):
    model = user_additional_info
    context_object_name = "user"
    template_name = "user/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = user_additional_info.post.objects.all()
        return context


def user_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    user_to_follow_profile = get_object_or_404(
        user_additional_info, user=user_to_follow)

    logged_in_user = get_object_or_404(User, username=request.user)

    logged_in_user_profile = get_object_or_404(
        user_additional_info, user=logged_in_user)

    logged_in_user_profile.following.add(user_to_follow)

    user_to_follow_profile.follower.add(logged_in_user)
    user_to_follow_profile.save()
    logged_in_user_profile.save()
    print(request.path)
    return HttpResponseRedirect(reverse('user:followers_list'))


def user_unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    user_to_unfollow_profile = get_object_or_404(
        user_additional_info, user=user_to_unfollow)

    logged_in_user = get_object_or_404(User, username=request.user)

    logged_in_user_profile = get_object_or_404(
        user_additional_info, user=logged_in_user)

    logged_in_user_profile.following.remove(user_to_unfollow)

    user_to_unfollow_profile.follower.remove(logged_in_user)

    user_to_unfollow_profile.save()
    logged_in_user_profile.save()

    return HttpResponseRedirect(reverse('user:following_list'))


class followers_list(generic.ListView):
    model = user_additional_info
    context_object_name = "followers"

    template_name = "user/followers.html"

    def get_queryset(self):
        logged_in_user = get_object_or_404(User, username=self.request.user)
        logged_in_user_profile = get_object_or_404(
            user_additional_info, user=logged_in_user)
        return logged_in_user_profile.follower.all()


class following_list(generic.ListView):
    model = user_additional_info
    context_object_name = 'following'
    template_name = "user/following.html"

    def get_queryset(self):
        logged_in_user = get_object_or_404(User, username=self.request.user)
        logged_in_user_profile = get_object_or_404(
            user_additional_info, user=logged_in_user)
        return logged_in_user_profile.following.all()


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))
