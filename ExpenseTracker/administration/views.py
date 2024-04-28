from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import AddUserForm, AddAdminForm


# Create your views here.
from django.views import generic
from django.contrib.auth.models import User

# class UserListView(generic.ListView):
#     model = User

#     context_object_name = 'user_list'
#     template_name = 'administration/user_list.html'
#     queryset = User.objects


def home(request):
    user_list = User.objects.filter(groups__name = 'Student')
    count = User.objects.filter(groups__name = 'Student').count
    return render(request, 'administration/user_list.html', {"us_list": user_list, "number_of_users": count})

def user_view(request, pk):
    user = User.objects.get(username=pk)
    return render(request, "administration/user.html", context={"user": user})

def add_user(request):
    form = AddUserForm(request.POST or None)
    if request.method == "POST" :
        if form.is_valid():
            new_user = form.save()
            # messages.success(
            #     request, "A new User record was added successfully"
            # )
            return redirect("administration_home")
    return render(request, "administration/add_user.html", {"form": form})

def update_user(request, pk):
    current_user = User.objects.get(username=pk)
    form = AddUserForm(request.POST or None, instance = current_user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            # messages.success(
            #     request, "A current user record was updated."
            # )
            return redirect("administration_home")
    return render(request, "administration/update_user.html", {"form": form})
    
def delete_user(request, pk):
    user = User.objects.get(username = pk)
    user.delete()
    return redirect("administration_home")

def userForm(request):
    return render(request, 'administration/user_form.html', {})



def adminList(request):
    admin_list = User.objects.filter(groups__name = 'Administration')
    count = User.objects.filter(groups__name = 'Administration').count
    return render(request, 'administration/admin_list.html', {"admin_list": admin_list, "number_of_admins": count})

def admin_view(request, pk):
    admin = User.objects.get(username=pk)
    return render(request, "administration/admin.html", context={"admin": admin})

def add_admin(request):
    form = AddAdminForm(request.POST or None)
    if request.method == "POST" :
        if form.is_valid():
            new_admin = form.save()
            # messages.success(
            #     request, "A new User record was added successfully"
            # )
            return redirect("admin_list")
    return render(request, "administration/add_admin.html", {"form": form})

def update_admin(request, pk):
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

def delete_admin(request, pk):
    user = User.objects.get(username = pk)
    user.delete()
    return redirect("admin_list")

def adminForm(request):
    return render(request, 'administration/admin_form.html', {})