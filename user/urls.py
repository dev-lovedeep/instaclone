from django.urls import path
from .views import *
app_name = 'user'
urlpatterns = [
    path('login/', userlogin, name="login"),
    path('logout/', userlogout, name="logout"),
    path('signup/', usersignup, name="signup"),
    path('<str:username>/followers/',
         followers_list.as_view(), name="followers_list"),
    path('<str:username>/following/',
         following_list.as_view(), name="following_list"),
    path('follow/', user_follow, name="follow"),
    path('unfollow/', user_unfollow, name="unfollow"),
    path('<str:username>/', userprofile.as_view(), name="profile"),
    path('<slug:slug>/edit', edit_user_profile.as_view(), name="edit_profile"),

]
