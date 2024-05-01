from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import AddUserForm, AddAdminForm

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
        return render(request, "administration/user.html", context={"user": user})
    else: 
        return redirect('home')

def add_user(request):
    if request.user.is_staff:
        form = AddUserForm(request.POST or None)
        if request.method == "POST" :
            if form.is_valid():
                new_user = form.save()
                return redirect("administration_home")
        return render(request, "administration/add_user.html", {"form": form})
    else: 
        return redirect('home')
    
def update_user(request, pk):
    if request.user.is_staff:
        current_user = User.objects.get(username=pk)
        form = AddUserForm(request.POST or None, instance = current_user)
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
    
def userForm(request):
    if request.user.is_staff:
        return render(request, 'administration/user_form.html', {})
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
        form = AddAdminForm(request.POST or None)
        if request.method == "POST" :
            if form.is_valid():
                new_admin = form.save()
                # messages.success(
                #     request, "A new User record was added successfully"
                # )
                return redirect("admin_list")
        return render(request, "administration/add_admin.html", {"form": form})
    else: 
        return redirect('home')

def update_admin(request, pk):
    if request.user.is_staff:
        current_admin = User.objects.get(username=pk)
        form = AddAdminForm(request.POST or None, instance = current_admin)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                # messages.success(
                #     request, "A current user record was updated."
                # )
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

