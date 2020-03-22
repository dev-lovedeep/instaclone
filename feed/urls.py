
from django.urls import path
from .views import *
app_name = 'feed'
urlpatterns = [
    path('', newsfeed.as_view(), name='feed'),
    # path('post/', include('post.urls', namespace='post')),
]
