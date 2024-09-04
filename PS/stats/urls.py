from . import views
from django.urls import path

urlpatterns = [
    path('', views.stats, name='stats'),
]
