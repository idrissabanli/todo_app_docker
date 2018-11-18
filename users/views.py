from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.forms import UserRegisterForm
from users.models import MyUser
from django.shortcuts import render, HttpResponseRedirect


def user_registration(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if not form.is_valid():
                return render(request, 'users/registration.html',
                              {'form_reg': form})
            else:
                last_name = form.cleaned_data.get('last_name')
                first_name = form.cleaned_data.get('first_name')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                MyUser.objects.create_user(email=email, password=password,
                                           first_name=first_name, last_name=last_name)
                user = authenticate(username=email, password=password)
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'users/registration.html',
                          {'form_reg': UserRegisterForm()})
    else:
        return redirect('/')
