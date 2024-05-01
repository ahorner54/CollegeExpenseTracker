from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Semester, Income, Expense
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Semester, Income, Expense
from datetime import date, timedelta

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('administration_home')
        user_pk = request.user.pk
        semesters = Semester.objects.filter(student_id = user_pk)
        context = {
           'semester_list': semesters
        }
        return render(request, 'budget/home.html', context=context)
    
    return render(request, 'budget/home.html', {})

class CreateIncome(CreateView):
    model = Income
    fields = ['semester', 'amount', 'is_recurring', 'recurring_period', 'memo']
    template_name = 'budget/income_form.html'
    success_url = reverse_lazy('home')

class UpdateIncome(UpdateView):
    model = Income
    fields = ['amount', 'is_recurring', 'recurring_period', 'memo']
    template_name = 'budget/income_form.html'
    success_url = reverse_lazy('home')

class DeleteIncome(DeleteView):
    model = Income
    template_name = 'budget/income_confirm_delete.html'
    success_url = reverse_lazy('home')

class CreateExpense(CreateView):
    model = Expense
    fields = ['semester', 'amount', 'is_recurring', 'recurring_period', 'memo']
    template_name = 'budget/expense_form.html'
    success_url = reverse_lazy('home')

class UpdateExpense(UpdateView):
    model = Expense
    fields = ['amount', 'is_recurring', 'recurring_period', 'memo']
    template_name = 'budget/expense_form.html'
    success_url = reverse_lazy('home')

class DeleteExpense(DeleteView):
    model = Expense
    template_name = 'budget/expense_confirm_delete.html'
    success_url = reverse_lazy('home')

class CreateSemester(CreateView):
    model = Semester
    fields = ['student', 'semester_name', 'start_date', 'end_date', 'starting_balance', 'semester_tuition', 'current_balance']
    template_name = 'budget/semester_form.html'
    success_url = reverse_lazy('home')

class DeleteSemester(DeleteView):
    model = Semester
    template_name = 'budget/semester_confirm_delete.html'
    success_url = reverse_lazy('home')

def semester(request, pk):
    if not(request.user.is_authenticated):
        return redirect('home')
    else:
        
        user_pk = request.user.pk
        semesters = Semester.objects.filter(student_id = user_pk)

        current_semester = Semester.objects.get(pk=pk)
        #current_semester.current_balance = 30000
        #current_semester.save()

        incomes = Income.objects.filter(semester_id=pk)
        expenses = Expense.objects.filter(semester_id=pk)
        semester_name = semesters[0].semester_name
        starting_balance = semesters[0].starting_balance

        #calculate to date expenses and income
        to_date_expense = to_date_sum(expenses)
        to_date_income = to_date_sum(incomes)

        #calculate current bal
        current_bal = current_semester.current_balance + (to_date_income - to_date_expense)
        current_semester.current_balance = current_bal
        current_semester.save()

        #calculate current to end income and expense
        end_income = end_sum(incomes)
        end_expense = end_sum(expenses)

        #calculate end bal
        end_balance = current_bal + (end_income - end_expense)

        context = {
           'semester_list': semesters,
           'semester_name': semester_name,
           'incomes': incomes,
            'expenses': expenses,
            'start_bal': starting_balance,
            'current_bal': current_bal,
            'end_bal': end_balance,

        }
        return render(request, 'budget/semester_view.html', context=context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Username and password do not match, try again.')
            return redirect('home')
    else:
        return render(request, 'budget/home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def to_date_sum(moneyList):
    total_money = 0
    #index 0 is leap year feb, rest are 1-12 for jan-dec
    days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]

    for record in moneyList: 
        #check date to see if needs update
        if record.is_recurring:
            last_updated = record.date_last_updated
            end_date = record.end_date
            period_days = 0
            match record.recurring_period:
                case 'weekly': 
                    period_days = 7
                case 'biweekly': 
                    period_days = 14

            if last_updated > end_date:
                continue

            #determine whether date.today() is later than end date, if so,
            # update based on last_update - end_date rather than
            # last_update - date.today()
            # This allows for balance to update if user has not checked in a while and checks after semester end
            period_end = date.today()
            if date.today() > end_date:
                period_end = end_date

            if record.recurring_period == 'weekly' or record.recurring_period == 'biweekly':
                #check if was updated in the past week
                if (period_end - last_updated ).days >= period_days:
                    days_since_updated = (period_end - last_updated).days
                    times_to_update = days_since_updated // period_days # num of periods to update

                    #update total_expense accordingly
                    total_money += (record.amount * times_to_update)

                    #set last_updated value to times_to_update * 7
                    new_date = record.date_last_updated + timedelta(days=(period_days*times_to_update))
                    current_record = Expense.objects.get(pk=record.pk)
                    current_record._date = new_date
                    current_record.save()

            elif record.recurring_period == 'monthly':
                #check if was updated in the past week
                if (period_end - last_updated).days >= days_in_month[period_end.month]:
                    days_since_updated = (period_end - last_updated).days
                    times_to_update = days_since_updated // days_in_month[period_end.month] # num of periods to update

                    #update total_expense accordingly
                    total_money += (record.amount * times_to_update)

                    #set last_updated value to times_to_update * month
                    current_month = record.date_last_updated.month
                    current_year = record.date_last_updated.year
                    days_to_add = 0
                    for i in range(0,times_to_update):
                        #check february of leap year
                        if(current_month == 2 and (current_year % 4 == 0 and not(current_year % 400 == 0))):
                            days_to_add += days_in_month[0]
                        else:
                            days_to_add += days_in_month[current_month]
                        #add to the month
                        currnet_month += 1
                        #if month == 13 update year and month
                        if current_month == 13:
                            current_year += 1
                            current_month=1
                        
                    new_date = record.date_last_updated + timedelta(days=(days_to_add))
                    current_record = Expense.objects.get(pk=record.pk)
                    current_record._date = new_date
                    current_record.save()
    return total_money

def end_sum(moneyList):
    total_money = 0
    days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31] #index 0 is leap year feb, rest are 1-12 for jan-dec

    for record in moneyList: 
        #check date to see if needs update
        if record.is_recurring:
            last_updated = record.date_last_updated
            end_date = record.end_date
            amount = record.amount
            period_days = 0
            match record.recurring_period:
                case 'weekly': 
                    period_days = 7
                case 'biweekly': 
                    period_days = 14

            if last_updated > end_date:
                continue

            if record.recurring_period == 'weekly' or record.recurring_period == 'biweekly':
                #check if was updated in the past week
                if (end_date - last_updated ).days >= period_days:
                    days_to_end = (end_date - last_updated).days
                    times_to_update = days_to_end // period_days # num of periods to update

                    #update total_expense accordingly
                    total_money += (amount * times_to_update)

            elif record.recurring_period == 'monthly':
                #check if was updated in the past week
                if (end_date - last_updated ).days >= days_in_month[end_date.month]:
                    days_to_end = (end_date - last_updated).days
                    times_to_update = days_to_end // days_in_month[end_date.month] # num of periods to update

                    #update total_expense accordingly
                    total_money += (amount * times_to_update)
    return total_money
