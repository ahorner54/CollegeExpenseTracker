from django.db import models
from django.conf import settings

# Create your models here.
class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    semester_name = models.CharField(max_length = 30)
    start_date = models.DateField()
    end_date = models.DateField()
    starting_balance = models.DecimalField(decimal_places=2, max_digits=10)
    semester_tuition = models.DecimalField(decimal_places=2, max_digits=10)
    #User Does Not Enter Expected End Balance, it is calculated
    current_balance = models.DecimalField(decimal_places=2, max_digits=10)

class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    semester_id = models.ForeignKey(Semester, on_delete=models.RESTRICT, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    is_recurring = models.BooleanField()
    #User Does Not Enter date_last_updated, it is automatically generated
    date_last_updated = models.DateField(auto_now=True)
    end_date = models.DateField()
    recurring_period = models.CharField(max_length = 20)
    memo = models.CharField(max_length=200, null=True)

class Expense(models.Model):
    income_id = models.AutoField(primary_key=True)
    semester_id = models.ForeignKey(Semester, on_delete=models.RESTRICT, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    is_recurring = models.BooleanField()
    #User Does Not Enter date_last_updated, it is automatically generated
    date_last_updated = models.DateField(auto_now=True)
    end_date = models.DateField()
    recurring_period = models.CharField(max_length = 20)
    memo = models.CharField(max_length=200, null=True)
