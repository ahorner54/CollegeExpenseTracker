from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('semester/<int:pk>', views.semester, name='semester'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('semester_form/', views.CreateSemester, name='semester_form'),
    path('income_form/<int:pk>', views.CreateIncome, name='income_form'),
    path('expense_form/<int:pk>', views.CreateExpense, name='expense_form'),

    path('stop_recur_income/<int:pk>', views.StopRecurringIncome, name='stop_income'),
    path('stop_recur_expense/<int:pk>/', views.StopRecurringExpense, name='stop_expense'),
    path('delete_semester/<int:pk>/', views.DeleteSemester, name='delete_semester'),

    path('account/<str:username>', views.view_account, name='account'),
    path('delete_account/<str:username>', views.delete_account, name='delete_account'),
]