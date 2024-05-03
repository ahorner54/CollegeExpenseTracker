from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import AddUserForm, UpdateUserForm
from django.contrib.auth.models import Group

# Create your views here.
from django.views import generic
from django.contrib.auth.models import User

def home(request):
    if request.user.is_staff:
        user_list = User.objects.filter( groups__name = 'Student')
        count = User.objects.filter(groups__name = 'Student').count
        return render(request, 'administration/user_list.html', {"us_list": user_list, "number_of_users": count})
    else:
        return redirect('home')

def user_view(request, pk):
    if request.user.is_staff:
        user = User.objects.get(username=pk)
        return render(request, "administration/user.html", context={"selected_user": user})
    else: 
        return redirect('home')

def add_user(request):
    if request.user.is_staff:
        form = AddUserForm(request.POST or None)
        if request.method == "POST" :
            if form.is_valid():
                new_user = form.save()
                student_group = Group.objects.get(name='Student')
                new_user.groups.add(student_group.id)
                return redirect("administration_home")
        return render(request, "administration/add_user.html", {"form": form})
    else: 
        return redirect('home')
    
def update_user(request, pk):
    if request.user.is_staff:
        current_user = User.objects.get(username=pk)
        form = UpdateUserForm(request.POST or None, instance = current_user)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect("administration_home")
        return render(request, "administration/update_user.html", {"form": form})
    else: 
        return redirect('home')
    
def delete_user(request, pk):
    if request.user.is_staff:
        user = User.objects.get(username = pk)
        user.delete()
        return redirect("administration_home")
    else: 
        return redirect('home')


def adminList(request):
    if request.user.is_staff:
        admin_list = User.objects.filter(groups__name = 'Administration')
        count = User.objects.filter(groups__name = 'Administration').count
        return render(request, 'administration/admin_list.html', {"admin_list": admin_list, "number_of_admins": count})
    else: 
        return redirect('home')

def admin_view(request, pk):
    if request.user.is_staff:
        admin = User.objects.get(username=pk)
        return render(request, "administration/admin.html", context={"admin": admin})
    else: 
        return redirect('home')

def add_admin(request):
    if request.user.is_staff:
        form = AddUserForm(request.POST or None)
        if request.method == "POST" :
            if form.is_valid():
                new_admin = form.save()
                new_admin.is_staff = True
                admin_group = Group.objects.get(name="Administration")
                new_admin.groups.add(admin_group.id)
                return redirect("admin_list")
        return render(request, "administration/add_admin.html", {"form": form})
    else: 
        return redirect('home')

def update_admin(request, pk):
    if request.user.is_staff:
        current_admin = User.objects.get(username=pk)
        form = UpdateUserForm(request.POST or None, instance = current_admin)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect("admin_list")
        return render(request, "administration/update_admin.html", {"form": form})
    else: 
        return redirect('home')

def delete_admin(request, pk):
    if request.user.is_staff:
        user = User.objects.get(username = pk)
        user.delete()
        return redirect("admin_list")
    else: 
        return redirect('home')

def change_password(request, pk):
    if request.user.is_staff:
        selected_user = User.objects.get(username = pk)
        if request.method == "POST":
            pass1 = str(request.POST.get('password1'))
            pass2 = str(request.POST.get('password2'))
            if pass1 == pass2:
                selected_user.set_password(pass1)
                selected_user.save()

            if selected_user.is_staff:
                return redirect('admin_list')
            return redirect('administration_home')
        return render(request, 'administration/update_password.html', {})
    return redirect('home')
