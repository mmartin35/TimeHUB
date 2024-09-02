from django.urls import path
from . import views

urlpatterns = [
    path('', views.disp_stats, name='disp_stats'),
]
