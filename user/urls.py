from django.urls import path, include
from .views import *

urlpatterns = [
    path('update-user', update_user),
    path('redis-cache', redis_cache),
]