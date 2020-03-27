from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def usersignup(request):
    if request.method == "POST":
        user_data = user_signup_form(data=request.POST)
        user_additional_data = user_additional_info_form(data=request.POST)
        print(user_data)
        if user_data.is_valid() and user_additional_data.is_valid():
            user = user_data.save()
            user.set_password(user.password)
            user.save()

            additional_data = user_additional_data.save(commit=False)
            additional_data.user = user
            additional_data.slug = slugify(additional_data.user.username)
            if 'profile_pic' in request.FILES:
                additional_data.profile_pic = request.FILES['profile_pic']
            additional_data.save()

            email = request.POST.get('email')
            firstname = request.POST.get('first_name')
            # email = user_data.get('email')
            print(email)
            subject = 'Thank you for registering'
            message = 'Dear {},\n thanks for registering to our website\n lovedeep singh\nadmin'.format(
                firstname)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            print(send_mail(subject, message, email_from, recipient_list))

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
            # if not get_user_model().objects.filter(username=username):
            if not get_object_or_404(User, username=username):
                return HttpResponse("no accout with username {} exist".format(username))
            else:
                return HttpResponse("invalid credentials")
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('feed:feed'))
        else:
            return render(request, "user/login.html", {})


class userprofile(LoginRequiredMixin, generic.ListView):
    model = user_additional_info
    # this is template name of queryset passed to the html page
    context_object_name = "user_profile"
    template_name = "user/profile.html"

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs['username'])
        user_profile = get_object_or_404(user_additional_info, user=user)
        return user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # this is the user whose profile is to be viewed
        user = get_object_or_404(User, username=self.kwargs['username'])
        user_profile = get_object_or_404(user_additional_info, user=user)
        # user_posts = get_object_or_404(Post, author=user)
        print(Post.objects.filter(author=user))
        context['followers'] = user_profile.follower.all()
        context['following'] = user_profile.following.all()
        context['posts'] = Post.objects.filter(author=user)
        return context

# fix it in next update


class edit_user_profile(LoginRequiredMixin, generic.UpdateView):
    model = user_additional_info
    fields = ['profile_pic', 'bio']
    template_name = 'user/edit_profile.html'
    # success_url = reverse_lazy('user:profile')

    def get_success_url(self, **kwargs):
        username = self.kwargs['slug']
        return reverse_lazy('user:profile', kwargs={'username': username})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = get_object_or_404(User, username=self.kwargs['slug'])
    #     context['img_url'] = get_object_or_404(
    #         user_additional_info, user=user).profile_pic.url


# def user_follow(request, username, calling_page_url):

@login_required
def user_follow(request):
    username = request.POST.get('user_to_follow')
    calling_page_url = request.POST.get('calling_page')
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
    print(username)
    print(calling_page_url)
    return HttpResponseRedirect(calling_page_url)
    # return HttpResponseRedirect(reverse('user:followers_list'))


@login_required
def user_unfollow(request):
    username = request.POST.get('user_to_unfollow')
    calling_page_url = request.POST.get('calling_page')
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
    print(username)
    print(calling_page_url)
    return HttpResponseRedirect(calling_page_url)


class followers_list(LoginRequiredMixin, generic.ListView):
    model = user_additional_info
    context_object_name = "followers"

    template_name = "user/followers.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # logged in user
        logged_in_user = get_object_or_404(User, username=self.request.user)
        logged_in_user_profile = get_object_or_404(
            user_additional_info, user=logged_in_user)
        # logged in user following list and follower list
        context['logged_in_user_following_list'] = logged_in_user_profile.following.all()
        context['logged_in_user_follower_list'] = logged_in_user_profile.follower.all()
        # account which is under view
        user = get_object_or_404(User, username=self.kwargs['username'])
        user_profile = get_object_or_404(user_additional_info, user=user)
        # account which is under view following list
        context['user_follower_list'] = user_profile.follower.all()
        return context
        # return logged_in_user_profile.follower.all()


class following_list(LoginRequiredMixin, generic.ListView):
    model = user_additional_info
    context_object_name = 'following'
    template_name = "user/following.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # logged in user
        logged_in_user = get_object_or_404(User, username=self.request.user)
        logged_in_user_profile = get_object_or_404(
            user_additional_info, user=logged_in_user)
        # logged in user following list and follower list
        context['logged_in_user_follower_list'] = logged_in_user_profile.follower.all()
        context['logged_in_user_following_list'] = logged_in_user_profile.following.all()
        # account which is under view
        user = get_object_or_404(User, username=self.kwargs['username'])
        user_profile = get_object_or_404(user_additional_info, user=user)
        # account which is under view following list
        context['user_following_list'] = user_profile.following.all()
        return context
        # return logged_in_user_profile.following.all()


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))
