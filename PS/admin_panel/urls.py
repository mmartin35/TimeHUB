from . import views
from django.urls import path

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('admin_events/', views.admin_events_json, name='admin_events_json'),
    path('setup/', views.setup, name='setup'),
    path('individual_report/<str:username>/<int:month>', views.individual_report, name='individual_report'),
    path('global_report/<int:month>', views.global_report, name='global_report'),
]