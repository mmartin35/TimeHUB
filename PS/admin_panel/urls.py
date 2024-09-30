from . import views
from django.urls import path
from planning.views import events_json

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('admin_events/', views.admin_events_json, name='admin_events_json'),
    path('setup/', views.setup, name='setup'),
]
