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
                recur_per = 'Not Recurring'
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
            return semester(request, current_semester.pk)
        return render(request, 'budget/income_form.html')
    else:
        return redirect('home')

def StopRecurringIncome(request, pk):
    if request.user.is_authenticated:
        income = Income.objects.get(pk=pk)
        if date.today() < income.end_date:
            income.end_date = date.today()
            income.save()
        
        return semester(request, income.semester_id.pk)
    else:
        return redirect('home')

def CreateExpense(request, pk):
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
                recur_per = 'Not Recurring'
                end_date = date.today()

            expense = Expense.objects.create(
                semester_id=current_semester,
                amount=float(amount),
                is_recurring=is_rec,
                recurring_period=recur_per,
                end_date = end_date,
                memo=request.POST.get('memo')
            )
            expense.save()
            return semester(request, current_semester.pk)
        return render(request, 'budget/expense_form.html')
    else:
        return redirect('home')

def StopRecurringExpense(request, pk):
    if request.user.is_authenticated:
        expense = Expense.objects.get(pk=pk)
        
        if date.today() < expense.end_date:
            expense.end_date = date.today()
            expense.save()

        return semester(request, expense.semester_id.pk)
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
           'current_semester': current_semester.pk,
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
