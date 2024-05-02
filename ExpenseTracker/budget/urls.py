from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('semester/<int:pk>', views.semester, name='semester'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('semester_form/', views.CreateSemester, name='semester_form'),
    path('income_form/<int:pk>', views.CreateIncome, name='income_form'),
    path('expense_form/', views.CreateExpense, name='expense_form')
]