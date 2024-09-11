from . import views
from django.urls import path

urlpatterns = [
    path('', views.planning, name='planning'),
    path('events/', views.events_json, name='events_json'),
]
