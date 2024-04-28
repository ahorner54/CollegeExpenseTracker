from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='administration_home'),
    path('user/<str:pk>', views.user_view, name='user_detail'),
    path('addUser/', views.add_user, name="add_user"),
    path("update_user/<str:pk>", views.update_user, name = "update_user"),
    path("delete_user/<str:pk>", views.delete_user, name = "delete_user"),
    
    path('admin_list/', views.adminList, name='admin_list'),
    path('admin/<str:pk>', views.admin_view, name='admin_detail'),
    path('addAdmin/', views.add_admin, name="add_admin"),
    path("update_admin/<str:pk>", views.update_admin, name = "update_admin"),
    path("delete_admin/<str:pk>", views.delete_user, name = "delete_admin"),
]