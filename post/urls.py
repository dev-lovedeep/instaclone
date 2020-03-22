from django.urls import path
from .views import *
app_name = 'post'
urlpatterns = [
    path('', post_create_view.as_view(), name="create"),
    path('<int:pk>/update', post_update_view.as_view(), name="update"),
    path('<int:pk>/delete', post_delete_view.as_view(), name="delete"),

]
