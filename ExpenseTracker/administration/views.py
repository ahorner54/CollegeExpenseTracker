from django.shortcuts import render

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
    return render(request, 'administration/user_list.html', {"us_list": user_list})

def user_view(request, pk):
    user = User.objects.get(username=pk)
    return render(request, "administration/user.html", context={"user": user})


def adminList(request):
    return render(request, 'administration/admin_list.html', {})


def userForm(request):
    return render(request, 'administration/user_form.html', {})