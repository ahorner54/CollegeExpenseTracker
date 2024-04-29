from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Semester, Income, Expense
from datetime import date, timedelta

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user_pk = request.user.pk
        semesters = Semester.objects.filter(student_id = user_pk)
        context = {
           'semester_list': semesters
        }
        return render(request, 'budget/home.html', context=context)
    
    return render(request, 'budget/home.html', {})

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

        #calculate total expense update
        total_expense = 0
        for expense in expenses: 
            #check date to see if needs update
            if expense.is_recurring:
                last_updated = expense.date_last_updated
                end_date = expense.end_date

                if last_updated > end_date:
                    continue

                if expense.recurring_period == 'weekly':
                    #check if was updated in the past week
                    if (date.today() - last_updated ).days >= 7:
                        days_since_updated = last_updated - date.today()
                        times_to_update = days_since_updated // 7 # num of periods to update

                        #update total_expense accordingly
                        total_expense += (expense.amount * times_to_update)

                        #set last_updated value to times_to_update * 7
                        new_date = expense.date_last_updated + timedelta(days=(7*times_to_update))
                        current_expense = Expense.objects.get(pk=expense.pk)
                        current_expense._date = new_date
                        current_expense.save()

                elif expense.recurring_period == 'biweekly':
                    #check if was updated in the past week
                    if (date.today() - last_updated).days >= 14:
                        days_since_updated = last_updated - date.today()
                        times_to_update = days_since_updated // 14 # num of periods to update

                        #update total_expense accordingly
                        total_expense += (expense.amount * times_to_update)

                        #set last_updated value to times_to_update * 14
                        new_date = expense.date_last_updated + timedelta(days=(14*times_to_update))
                        current_expense = Expense.objects.get(pk=expense.pk)
                        current_expense._date = new_date
                        current_expense.save()

                elif expense.recurring_period == 'monthly':
                    #index 0 is leap year feb, rest are 1-12 for jan-dec
                    days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]
                    #check if was updated in the past week
                    if (date.today() - last_updated).days >= days_in_month[date.today().month]:
                        days_since_updated = last_updated - date.today()
                        times_to_update = days_since_updated // days_in_month[date.today().month] # num of periods to update

                        #update total_expense accordingly
                        total_expense += (expense.amount * times_to_update)

                        #set last_updated value to times_to_update * month
                        current_month = expense.date_last_updated.month
                        current_year = expense.date_last_updated.year
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
                            
                        new_date = expense.date_last_updated + timedelta(days=(days_to_add))
                        current_expense = Expense.objects.get(pk=expense.pk)
                        current_expense._date = new_date
                        current_expense.save()
            

        #calculate total expense update
        total_income = 0
        for income in incomes: 
           #check date to see if needs update
            if income.is_recurring:
                last_updated = income.date_last_updated
                end_date = income.end_date

                if last_updated > end_date:
                    continue

                if income.recurring_period == 'weekly':
                    #check if was updated in the past week
                    if (date.today() - last_updated).days >= 7:
                        days_since_updated = last_updated - date.today()
                        times_to_update = days_since_updated // 7 # num of periods to update

                        #update total_expense accordingly
                        total_income += (income.amount * times_to_update)

                        #set last_updated value to times_to_update * 7
                        new_date = income.date_last_updated + timedelta(days=(7*times_to_update))
                        currnet_income = Income.objects.get(pk=income.pk)
                        currnet_income._date = new_date
                        currnet_income.save()

                elif income.recurring_period == 'biweekly':
                    #check if was updated in the past week
                    if (date.today() - last_updated).days >= 14:
                        days_since_updated = last_updated - date.today()
                        times_to_update = days_since_updated // 14 # num of periods to update

                        #update total_expense accordingly
                        total_income += (income.amount * times_to_update)

                        #set last_updated value to times_to_update * 14
                        new_date = income.date_last_updated + timedelta(days=(14*times_to_update))
                        currnet_income = Income.objects.get(pk=income.pk)
                        currnet_income._date = new_date
                        currnet_income.save()

                elif income.recurring_period == 'monthly':
                    #index 0 is leap year feb, rest are 1-12 for jan-dec
                    days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]
                    #check if was updated in the past week
                    if (date.today() - last_updated).days >= days_in_month[date.today().month]:
                        days_since_updated = last_updated - date.today()
                        times_to_update = days_since_updated // days_in_month[date.today().month] # num of periods to update

                        #update total_expense accordingly
                        total_income += (income.amount * times_to_update)

                        #set last_updated value to times_to_update * month
                        current_month = income.date_last_updated.month
                        current_year = income.date_last_updated.year
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
                            
                        new_date = income.date_last_updated + timedelta(days=(days_to_add))
                        currnet_income = Income.objects.get(pk=income.pk)
                        currnet_income._date = new_date
                        currnet_income.save()


        
        #calculate current bal
        current_bal = current_semester.current_balance + total_income - total_expense
        current_semester.current_balance = current_bal
        current_semester.save()

        #calculate current to end income
        end_income = 0
        for income in incomes: 
           #check date to see if needs update
            if income.is_recurring:
                last_updated = income.date_last_updated
                end_date = income.end_date

                if last_updated > end_date:
                    continue

                if income.recurring_period == 'weekly':
                    #check if was updated in the past week
                    if (end_date - last_updated ).days >= 7:
                        days_to_end = last_updated - end_date
                        times_to_update = days_to_end // 7 # num of periods to update

                        #update total_expense accordingly
                        end_income += (income.amount * times_to_update)

                elif income.recurring_period == 'biweekly':
                    #check if was updated in the past week
                    if (end_date - last_updated ).days >= 14:
                        days_to_end = last_updated - end_date
                        times_to_update = days_to_end // 14 # num of periods to update

                        #update total_expense accordingly
                        end_income += (income.amount * times_to_update)

                elif income.recurring_period == 'monthly':
                    #index 0 is leap year feb, rest are 1-12 for jan-dec
                    days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]
                    #check if was updated in the past week
                    if (end_date - last_updated ).days >= days_in_month[date.today().month]:
                        days_to_end = last_updated - end_date
                        times_to_update = days_to_end // days_in_month[date.today().month] # num of periods to update

                        #update total_expense accordingly
                        end_icnome += (income.amount * times_to_update)

        #calculate current to end expense
        end_expense = 0
        for expense in expenses: 
           #check date to see if needs update
            if expense.is_recurring:
                last_updated = expense.date_last_updated
                end_date = expense.end_date

                if last_updated > end_date:
                    continue

                if expense.recurring_period == 'weekly':
                    #check if was updated in the past week
                    if (end_date - last_updated ).days >= 7:
                        days_to_end = last_updated - end_date
                        times_to_update = days_to_end // 7 # num of periods to update

                        #update total_expense accordingly
                        end_expense += (expense.amount * times_to_update)

                elif expense.recurring_period == 'biweekly':
                    #check if was updated in the past week
                    if (end_date - last_updated ).days >= 14:
                        days_to_end = last_updated - end_date
                        times_to_update = days_to_end // 14 # num of periods to update

                        #update total_expense accordingly
                        end_expense += (expense.amount * times_to_update)

                elif expense.recurring_period == 'monthly':
                    #index 0 is leap year feb, rest are 1-12 for jan-dec
                    days_in_month = [29,31,28,31,30,31,30,31,31,30,31,30,31]
                    #check if was updated in the past week
                    if (end_date - last_updated ).days >= days_in_month[date.today().month]:
                        days_to_end = last_updated - end_date
                        times_to_update = days_to_end // days_in_month[date.today().month] # num of periods to update

                        #update total_expense accordingly
                        end_expense += (expense.amount * times_to_update)

        #calculate end bal
        end_balance = current_bal + end_income - end_expense

        context = {
           'semester_list': semesters,
           'semester_name': semester_name,
           'incomes': incomes,
            'expenses': expenses,
            'start_bal': starting_balance,
            'current_bal': current_bal,
            'end_bal': end_balance

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