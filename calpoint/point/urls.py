from django.urls import path
from . import views

urlpatterns = [
    path('', views.pointing, name='pointing'),
]
