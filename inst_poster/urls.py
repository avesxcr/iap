from django.urls import path
from .views import *

urlpatterns = [
    path('poster', poster, name='poster'),
]