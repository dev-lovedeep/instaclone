from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .signupform import user_signup_form
# Create your views here.


class newuser(generic.CreateView):
    model = User
    template_name = 'user/signup.html'
    form_class = user_signup_form
    # fields = ('username', 'first_name', 'last_name', 'password', 'email')
    success_url = '/accounts/login'


def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url and next_url != '/':
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse('feed:feed'))
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
