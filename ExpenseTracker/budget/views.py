from django.shortcuts import render, redirect # type: ignore
from django.views.generic import CreateView, UpdateView, DeleteView # type: ignore
from django.urls import reverse_lazy # type: ignore
from .models import Semester, Income, Expense
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from django.views import generic # type: ignore
from .models import Semester, Income, Expense
from datetime import date, timedelta
from django import forms  # type: ignore
from django.contrib.auth.decorators import login_required, permission_required # type: ignore

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

def CreateIncome(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_semester = Semester.objects.get(pk=pk)
            current_balance = current_semester.current_balance
            amount = request.POST.get('amount')
            cur_bal = float(current_balance) + float(amount)
            current_semester.current_balance = cur_bal
            current_semester.save()
            is_rec = request.POST.get('is_recurring')
            if is_rec == 'Yes':
                is_rec = True
                recur_per = request.POST.get('recurring_period')
                end_date = request.POST.get('end_date')
            else:
                is_rec = False
                recur_per = 'Not today pal'
                end_date = date.today()

            income = Income.objects.create(
                semester_id=current_semester,
                amount=float(amount),
                is_recurring=is_rec,
                recurring_period=recur_per,
                end_date = end_date,
                memo=request.POST.get('memo')
            )
            income.save()
            return redirect('home')
        return render(request, 'budget/income_form.html')
    else:
        return redirect('home')

def DeleteIncome(request, pk):
    if request.user.is_authenticated:
        income = Income.objects.get(pk=pk)
        if request.method == 'POST':
            income.delete()
            return redirect('home')
        return render(request, 'budget/income_confirm_delete.html', {'income': income})
    else:
        return redirect('home')

def CreateExpense(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            start_bal = request.POST.get('amount')
            sem_tuit = request.POST.get('semester__semester_tuition')
            cur_bal = float(start_bal) - float(sem_tuit)

            expense = Expense.objects.create(
                semester_id=request.POST.get('semester'),
                amount=float(start_bal),
                is_recurring=request.POST.get('is_recurring'),
                recurring_period=request.POST.get('recurring_period'),
                memo=request.POST.get('memo'),
                current_balance=cur_bal
            )
            expense.save()
            return redirect('home')
        return render(request, 'budget/expense_form.html')
    else:
        return redirect('home')

def DeleteExpense(request, pk):
    if request.user.is_authenticated:
        expense = Expense.objects.get(pk=pk)
        if request.method == 'POST':
            expense.delete()
            return redirect('home')
        return render(request, 'budget/expense_confirm_delete.html', {'expense': expense})
    else:
        return redirect('home')

def CreateSemester(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            start_bal = request.POST.get('starting_balance'),
            sem_tuit = request.POST.get('semester_tuition'),
            cur_bal = (float(start_bal[0]) - float(sem_tuit[0]))


            semester = Semester.objects.create(
                student_id = request.user,
                semester_name = request.POST.get('semester_name'),
                start_date = request.POST.get('start_date'),
                end_date = request.POST.get('end_date'),
                starting_balance = float(start_bal[0]),
                semester_tuition = float(sem_tuit[0]),
                current_balance = cur_bal
            )
            semester.save()
            return redirect('home')
        return render(request, 'budget/semester_form.html')
    else:
        return redirect('home')

def DeleteSemester(request, pk):
    if request.user.is_authenticated:
        semester = Semester.objects.get(pk=pk)
        if request.method == 'POST':
            semester.delete()
            return redirect('home')
        return render(request, 'budget/semester_confirm_delete.html', {'semester': semester})
    else:
        return redirect('home')

class SemesterForm(forms.ModelForm):
        class Meta:
            model = Semester
            fields = ['semester_name', 'start_date', 'end_date', 'starting_balance', 'semester_tuition', 'current_balance']

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
        semester_name = current_semester.semester_name
        starting_balance = current_semester.starting_balance

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
           'current_semester': current_semester.pk,
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
    for record in moneyList: 
        #check date to see if needs update
        if record.is_recurring:
            last_updated = record.date_last_updated
            end_date = record.end_date

            if last_updated > end_date:
                continue

            if record.recurring_period == 'weekly':
                #check if was updated in the past week
                if (date.today() - last_updated ).days >= 7:
                    days_since_updated = (date.today() - last_updated).days
                    times_to_update = days_since_updated // 7 # num of periods to update

                    #update total_expense accordingly
                    total_money += (record.amount * times_to_update)

                    #set last_updated value to times_to_update * 7
                    new_date = record.date_last_updated + timedelta(days=(7*times_to_update))
                    current_record = Expense.objects.get(pk=record.pk)
                    current_record._date = new_date
                    current_record.save()

            elif record.recurring_period == 'biweekly':
                #check if was updated in the past week
                if (date.today() - last_updated).days >= 14:
                    days_since_updated = (date.today() - last_updated).days
                    times_to_update = days_since_updated // 14 # num of periods to update

                    #update total_expense accordingly
                    total_money += (record.amount * times_to_update)

                    #set last_updated value to times_to_update * 14
                    new_date = record.date_last_updated + timedelta(days=(14*times_to_update))
                    current_record = Expense.objects.get(pk=record.pk)
                    current_record._date = new_date
                    current_record.save()

            elif record.recurring_period == 'monthly':
                #index 0 is leap year feb, rest are 1-12 for jan-dec
                days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]
                #check if was updated in the past week
                if (date.today() - last_updated).days >= days_in_month[date.today().month]:
                    days_since_updated = (date.today() - last_updated).days
                    times_to_update = days_since_updated // days_in_month[date.today().month] # num of periods to update

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
    for record in moneyList: 
        #check date to see if needs update
        if record.is_recurring:
            last_updated = record.date_last_updated
            end_date = record.end_date
            amount = record.amount

            if last_updated > end_date:
                continue

            if record.recurring_period == 'weekly':
                #check if was updated in the past week
                if (end_date - last_updated ).days >= 7:
                    days_to_end = (end_date - last_updated).days
                    times_to_update = days_to_end // 7 # num of periods to update

                    #update total_expense accordingly
                    total_money += (amount * times_to_update)

            elif record.recurring_period == 'biweekly':
                #check if was updated in the past week
                if (end_date - last_updated ).days >= 14:
                    days_to_end = (end_date - last_updated).days
                    times_to_update = days_to_end // 14 # num of periods to update

                    #update total_expense accordingly
                    total_money += (amount * times_to_update)

            elif record.recurring_period == 'monthly':
                #index 0 is leap year feb, rest are 1-12 for jan-dec
                days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]
                #check if was updated in the past week
                if (end_date - last_updated ).days >= days_in_month[date.today().month]:
                    days_to_end = (end_date - last_updated).days
                    times_to_update = days_to_end // days_in_month[date.today().month] # num of periods to update

                    #update total_expense accordingly
                    total_money += (amount * times_to_update)
    return total_money


    