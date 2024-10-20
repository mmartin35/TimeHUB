from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin_events/', views.admin_events_json, name='admin_events_json'),
    path('set_intern/', views.set_intern, name='set_intern'),
    path('set_data/', views.set_data, name="set_data"),
    path('set_publicholiday/', views.set_publicholiday, name='set_publicholiday'),
    path('preview_report', views.preview_report, name='preview_report'),
    path('individual_report/<str:username>/<int:month>', views.individual_report, name='individual_report'),
    path('global_report/<int:month>', views.global_report, name='global_report'),
]