from django.contrib import admin
from .models import Semester, Income, Expense

# Register your models here.
admin.site.register(Semester)
admin.site.register(Income)
admin.site.register(Expense)