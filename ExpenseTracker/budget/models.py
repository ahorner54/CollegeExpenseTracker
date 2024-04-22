from django.db import models
from django.conf import settings

# Create your models here.
class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    starting_balance = models.DecimalField()
    semester_tuition = models.DecimalField()
    #User Does Not Enter Expected End Balance, it is calculated
    expected_end_balance = starting_balance

class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    semester_id = models.ForeignKey(Semester, on_delete=models.models.RESTRICT, null=True)
    amount = models.DecimalField()
    is_recurring = models.BooleanField()
    #User Does Not Enter date_last_updated, it is automatically generated
    date_last_updated = models.DateField(auto_now=True)
    recurring_period = models.CharField(max_length = 20)
    memo = models.CharField(max_length=200, null=True)

class Expense(models.Model):
    income_id = models.AutoField(primary_key=True)
    semester_id = models.ForeignKey(Semester, on_delete=models.models.RESTRICT, null=True)
    amount = models.DecimalField()
    is_recurring = models.BooleanField()
    #User Does Not Enter date_last_updated, it is automatically generated
    date_last_updated = models.DateField(auto_now=True)
    recurring_period = models.CharField(max_length = 20)
    memo = models.CharField(max_length=200, null=True)
