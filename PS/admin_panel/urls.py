from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin_events/', views.admin_events_json, name='admin_events_json'),
    path('create_intern/', views.create_intern, name='create_intern'),
    path('edit_data/', views.edit_data, name="edit_data"),
    path('individual_report/<str:username>/<int:month>', views.individual_report, name='individual_report'),
    path('global_report/<int:month>', views.global_report, name='global_report'),
]