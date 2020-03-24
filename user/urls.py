from django.urls import path
from .views import *
app_name = 'user'
urlpatterns = [
    path('<int:pk>/', userprofile.as_view(), name="profile"),
    path('login/', userlogin, name="login"),
    path('logout/', userlogout, name="logout"),
    path('signup/', usersignup, name="signup"),
    path('followers/', followers_list.as_view(), name="followers_list"),
    path('following/', following_list.as_view(), name="following_list"),
    path('follow/<str:username>/', user_follow, name="follow"),
    path('unfollow/<str:username>/', user_unfollow, name="unfollow"),

]
