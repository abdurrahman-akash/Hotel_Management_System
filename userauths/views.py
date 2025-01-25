from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from userauths.forms import UserRegisterForm
from userauths.models import User, Profile


def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('hotel:index')

    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get('full_name')
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)
        login(request, user)

        messages.success(request, f'Hey, {username}! Your account has been created successfully.')

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone 
        profile.save()


        return redirect('hotel:index')

    context = {
        'form': form
    }

    return render(request, 'userauths/register.html', context)


