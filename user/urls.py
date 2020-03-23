from django.urls import path
from .views import *
app_name = 'user'
urlpatterns = [
    path('login/', userlogin, name="login"),
    path('logout/', userlogout, name="logout"),
    path('signup/', usersignup, name="signup"),
]
