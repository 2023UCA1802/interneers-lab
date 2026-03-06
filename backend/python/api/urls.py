from django.urls import path
from .view import greet

urlpatterns = [
    path("greet/", greet),
]