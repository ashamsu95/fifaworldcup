from django.shortcuts import render

# Create your views here.


from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from . import forms
from user.models import MyUser,addduser_number

def addnumber(request):
    if request.user.is_staff:
        form = forms.phone(request.POST or None)
        context = {
         'form': form
         }
        if form.is_valid():
            phone=form.cleaned_data.get("phone_number")
            addduser_number.objects.create(phone=phone,user=request.user)
            messages.error(request,"user phone added")
            return redirect('/authuser/fixtures')
        return render(request, "user/registerphone.html", context=context)
    else:
        return redirect('/')

# Create your views here.
def loginuser(request):
    if request.user.is_anonymous:
        form = forms.LoginForm(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            email = form.cleaned_data.get('Email')
            password = form.cleaned_data.get('password')
            try:
                qs = get_user_model().objects.filter(email=email).get()
            except ObjectDoesNotExist:
                messages.error(request,'email doest not exits')
                return render(request, "user/login.html", context=context)
            user = authenticate(request, username=qs, password=password)
            if user is not None:
                login(request, user)
                return redirect('authuser/fixtures')        
            else:
                messages.error(request,'Email or password not correct')
                return render(request, "user/login.html", context=context)
        return render(request, "user/login.html", context=context)
    elif request.user.is_anonymous == False:
        messages.error(request,"Welcome Back")
        return redirect('/authuser/fixtures')

def register_page(request):
    form = forms.RegisterForm(request.POST or None)
    # team = forms.Team()
    context = {
        'form': form,
        # 'team': team,
    }
    if form.is_valid():
        firstname = form.cleaned_data.get("First_Name") 
        lastname = form.cleaned_data.get("Last_Name")
        Email = form.cleaned_data.get("email")
        Password = form.cleaned_data.get("password_first")
        phone=form.cleaned_data.get("phone_number")
        userteam = request.POST["team"]
        if addduser_number.objects.filter(phone=phone,alreadyuser= False).exists():
            up = addduser_number.objects.get(phone=phone,alreadyuser= False)
            newuser = get_user_model().objects.create_user(username= firstname + lastname ,email=Email,password=Password,first_name=firstname,last_name=lastname)
            my_user = MyUser()
            my_user.user = newuser
            my_user.phone = phone
            my_user.team = userteam
            my_user.save()
            up.alreadyuser = True
            up.save()
            qs = get_user_model().objects.filter(email=Email).get()
            user = authenticate(request, username=qs, password=Password)
            if user is not None:
                login(request, user)
                return redirect('authuser/fixtures') 
            else:
                return redirect('/')
        else:
            messages.error(request,"The phone number is not registered")
            return render(request, 'user/register.html', context=context)
    return render(request, 'user/register.html', context=context)

@login_required
def logout_page(request):
    logout(request)
    messages.error(request,'You have logged out')
    return redirect('/')



