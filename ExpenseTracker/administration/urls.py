from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='administration_home'),
    path('admin_list/', views.adminList, name='admin_list'),
    path('', views.userForm, name='user_form'),
]