from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'administration/user_list.html', {})


def adminList(request):
    return render(request, 'administration/admin_list.html', {})

def userForm(request):
    return render(request, 'administration/user_form.html', {})