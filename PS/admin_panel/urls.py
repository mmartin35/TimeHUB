from . import views
from django.urls import path

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('archive/', views.archive, name='archive'),
]
