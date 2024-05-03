from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import Group

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            student_group = Group.objects.get(name='Student')
            new_user.groups.add(student_group.id)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        
    else:
        form = SignUpForm()
        
    return render(request, 'registration/register.html', {'form':form})