from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.pointer, name='pointer'),
        path('login/', views.login_view, name='login'),
        path('account/', views.callback, name='callback'),
        path('account/login/', views.login_allauth, name='login_allauth'),
        path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]