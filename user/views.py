from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
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


@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))
