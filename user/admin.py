from django.contrib import admin
from .models import follow, user_additional_info
# Register your models here.
admin.site.register(user_additional_info)
admin.site.register(follow)
