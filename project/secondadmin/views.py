from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from booking.models import Booking_Details
from user.models import User
from mentor.models import Mentor
import datetime
from datetime import date


def all_logout2(request):
   try: 
        user=request.user 
        if user.user_role=='student' or user.user_role=='mentor':
            logout(request)     
        return redirect(adminlogin)
   except:
       return redirect(adminlogin)

def adminlogin(request):
    all_logout2(request)
    if request.user.is_authenticated:
        return redirect(adminhome)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_admin==True:
            login(request, user)
            return redirect(adminhome)
        else:
            messages.error(request,'invalid credentials')

    return render(request, 'adminlogin.html')
    
def adminhome(request):
    all_logout2(request)
    users=User.objects.filter(user_role='student').order_by('is_active')
    context={
        'users':users
    }

    if request.user.is_authenticated:
        return render(request, 'adminhome.html',context)
    return redirect(adminlogin)    

def adminlogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(adminlogin)     
    
def adminmentor(request):
    all_logout2(request)
    
    mentors=Mentor.objects.all().order_by('id')
    context={
        'mentors':mentors,
    }

    if request.user.is_authenticated:
        return render(request, 'adminmentor.html',context)
    return redirect(adminlogin)    

def adminbooking(request):
    all_logout2(request)
    bookings=Booking_Details.objects.all()
    today=date.today()
    context={
        'bookings':bookings,
        'today':today
    }
    if request.user.is_authenticated:
      return render(request, 'adminbooking.html',context) 
    return redirect(adminlogin)   

def adminblock(request,id):
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect(adminhome)
    
def adminunblock(request,id):
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect(adminhome)      

def mentorblock(request,id):
    mentor=Mentor.objects.get(id=id)
    mentor.is_verified=False
    mentor.save()
    return redirect(adminmentor)
    
def mentorunblock(request,id):
    mentor=Mentor.objects.get(id=id)
    mentor.is_verified=True
    mentor.save()
    return redirect(adminmentor)       


    