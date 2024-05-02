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
from dateutil.relativedelta import relativedelta

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
        incomes = Income.objects.filter(semester_id=pk)
        expenses = Expense.objects.filter(semester_id=pk)
        semester_name = current_semester.semester_name
        starting_balance = current_semester.starting_balance
        tuition = current_semester.semester_tuition

        test_expense = Expense.objects.get(memo='test expense')

        testexpenselu = test_expense.date_last_updated
        #calculate to date expenses and income
        to_date_expense = to_date_sum(expenses, False)
        to_date_income = to_date_sum(incomes, True)

        #calculate current bal
        current_bal = current_semester.current_balance + (to_date_income - to_date_expense)
        current_semester.current_balance = current_bal
        current_semester.save()

        #calculate current to end income and expense
        end_income = end_sum(incomes)
        end_expense = end_sum(expenses)

        #calculate end bal
        end_balance = current_bal + (end_income - end_expense)

        #Get income and expense summaries
        income_summary = {'weekly': 0, 'biweekly': 0, 'monthly': 0}
        for income in incomes:
            if income.is_recurring:
                match income.recurring_period:
                    case 'weekly': income_summary['weekly'] += income.amount
                    case 'biweekly': income_summary['biweekly'] += income.amount
                    case 'monthly': income_summary['monthly'] += income.amount

        expense_summary = {'weekly': 0, 'biweekly': 0, 'monthly': 0} 
        for expense in expenses:
            if expense.is_recurring:
                match expense.recurring_period:
                    case 'weekly': expense_summary['weekly'] += expense.amount
                    case 'biweekly': expense_summary['biweekly'] += expense.amount
                    case 'monthly': expense_summary['monthly'] += expense.amount

        context = {
           'semester_list': semesters,
           'semester_name': semester_name,
           'incomes': incomes,
            'expenses': expenses,
            'start_bal': starting_balance,
            'current_bal': current_bal,
            'end_bal': end_balance,
            'income_weekly': income_summary['weekly'],
            'income_biweekly': income_summary['biweekly'],
            'income_monthly': income_summary['monthly'],
            'expense_weekly': expense_summary['weekly'],
            'expense_biweekly': expense_summary['biweekly'],
            'expense_monthly': expense_summary['monthly'],
            'tuition': tuition,
            'ts_lu': testexpenselu
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

def to_date_sum(moneyList, is_income):
    total_money = 0

    for record in moneyList: 
        #check date to see if needs update
        if record.is_recurring:
            last_updated = record.date_last_updated
            end_date = record.end_date
            period_days = 200
            match record.recurring_period:
                case 'weekly': 
                    period_days = 7
                case 'biweekly': 
                    period_days = 14

            if last_updated > end_date:
                continue

            #determine whether date.today() is later than end date, if so, update based on last_update - end_date rather than
            # last_update - date.today(); this allows for balance to update if user has not checked in a while and checks after semester end
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
                    if is_income:
                        current_record = Income.objects.get(pk=record.pk)
                    else:
                        current_record = Expense.objects.get(pk=record.pk)
                    current_record.date_last_updated = new_date
                    current_record.save()

            elif record.recurring_period == 'monthly':
                #check if was updated in the past week
                if relativedelta(period_end, last_updated).months >= 1:
                    months_since_updated = relativedelta(period_end, last_updated).months

                    #update total_expense accordingly
                    total_money += (record.amount * months_since_updated)

                    new_date = record.date_last_updated + relativedelta(months=months_since_updated)
                    if is_income:
                        current_record = Income.objects.get(pk=record.pk)
                    else:
                        current_record = Expense.objects.get(pk=record.pk)
                    current_record.date_last_updated = new_date
                    current_record.save()

    return total_money

def end_sum(moneyList):
    total_money = 0

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
                if relativedelta(end_date, last_updated).months >= 1:
                    months_to_end = relativedelta(end_date, last_updated).months

                    #update total_money accordingly
                    total_money += (amount * months_to_end)

    return total_money