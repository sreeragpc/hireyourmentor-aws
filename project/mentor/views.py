from multiprocessing import context
from unicodedata import category
from xml import dom
from django.http import HttpResponse
from django.shortcuts import render,redirect
from booking.models import Booking_Details
from user.models import User
from mentor.models import Mentor, Qualification
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages,auth
from category.models import Category, Domains
from user.otp import verify, verify_check

def all_logout1(request):
   try: 
        user=request.user 
        if user.user_role=='student' or user.user_role=='admin':
            logout(request)     
        return redirect(mentorlogin)
   except:
       return redirect(mentorlogin)

def mentorlogin(request):
    all_logout1(request)
    if request.user.is_authenticated :
        return redirect(mentordash)
    if request.method == 'POST':
        email = request.POST['email']
        request.session['email'] = email 
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None and user.user_role=='mentor' and user.is_admin==False:
            login(request, user)
            return redirect(mentordash)
        else:
            messages.error(request,'invalid credentials')    
    return render(request, 'mentorlogin.html')

def mentordash(request):
    all_logout1(request)
    user=request.user
    user_id=user.id
    try: 
        mentor=Mentor.objects.get(mentoruser_id=user_id)
        cat_id=mentor.Cat_id
        dom_id=mentor.Dom_id
        qual_id=mentor.Qual_id
        dom=Domains.objects.get(id=dom_id)
        cat=Category.objects.get(id=cat_id)
        qual=Qualification.objects.get(id=qual_id)
    except:
        mentor=None
        dom=None
        cat=None
        qual=None
        mentor_image=None
    context={
        'dom':dom,
        'cat':cat,
        'mentor':mentor,
        'qual':qual
    }
    if request.user.is_authenticated:
        return render(request, 'mentordash.html',context)    
    return redirect(mentorlogin)  

def mentorlogout(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request,'mentorlogin.html')       

def mentorsignup(request):
 logout(request)   
 try:
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            request.session['username'] = username
            email = request.POST['email']
            request.session['email'] = email 
            city = request.POST['city']
            phone_number1 = request.POST['phone_number']
            verify(phone_number1)
            request.session['phone_number1'] = phone_number1
            password= request.POST['password']
            user = User.objects.create_user(first_name =first_name,last_name=last_name, username = username , email =email, city =city , phone_number = phone_number1,password = password)
            user.user_role = "mentor"
            user.is_active=False
            user.save()
            return redirect(mentorotp)
 except:
     messages.error(request,'Try with different email or phone number')
 return render(request, 'mentorsignup.html') 
    
def mentorotp(request):
    all_logout1(request)
    phone_number=request.session['phone_number1']
    try:
        user=User.objects.get(phone_number=phone_number)
        if request.method== 'POST':
            otp=request.POST['otp']
            if verify_check(phone_number,otp)==True:
                user.is_active=True
                user.save()
                return redirect(mentorlogin)
            else:
                messages.error(request,'Entered OTP is not correct!')
    except:
        messages.error(request,'try again !')
        return redirect(mentorsignup)          
    return render(request, 'mentorotp.html')
def mentoredit(request):
    all_logout1(request)
    try:
        user=request.user
        user_id=user.id
        mentor=Mentor.objects.get(mentoruser_id=user_id)
    except:
        mentor=Mentor.objects.create(mentoruser_id=user_id)
    cat=Category.objects.all()
    dom=Domains.objects.all()
    qual=Qualification.objects.all()
    context={
        'mentor':mentor,
        'cat':cat,
        'dom':dom,
        'qual':qual
        }
    try:
        if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            city=request.POST['city']
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.city=city
            user.save()
            mentor.is_verified=False
            domain=request.POST['domain']
            Qual=request.POST['qual']
            mentor_price=request.POST['price']
            description=request.POST['desc']
            if request.FILES['img'] :                
                mentor.mentor_image=request.FILES['img']            
            mentor.Dom_id=domain
            mentor.Qual_id=Qual
            cat=Domains.objects.get(id=domain)
            cate=cat.Category_id            
            mentor.Cat_id=cate
            mentor.mentor_desc=description
            mentor.mentor_price=mentor_price
            mentor.save()
            return redirect(mentordash)
    except:
        messages.error(request,'please enter values in all fields')
    if request.user.is_authenticated:
        return render(request,'mentoredit.html',context)  
    return redirect(mentorlogin)                     
    

def mentorbooking(request):
    all_logout1(request)
    user=request.user
    id=user.id
    try:
        mentor=Mentor.objects.get(mentoruser=id)
        mentor_id=mentor.id        
        bookings=Booking_Details.objects.filter(selected_mentor=mentor_id).order_by('slot_is_active')
    except:
        bookings=None    
    context={
        'bookings':bookings
    }
    if request.user.is_authenticated:
        return render(request,'mentorbooking.html',context)  
    return redirect(mentorlogin)      

def mentorpassword(request):
     all_logout1(request)
     user=request.user
     if request.method == 'POST':
        password = request.POST['current_password']
        if auth.authenticate(username=user.email,password=password):
            new_password=request.POST['password']
            password1=request.POST['password1']
            if new_password == password1:
                user.set_password(new_password)
                user.save()
                auth.login(request, user )
                return redirect(mentordash)
            else:
                messages.error(request, 'give same password')
        else:
            messages.error(request, 'wrong password')     
     if request.user.is_authenticated:
        return render(request,'mentorpassword.html')  
     return redirect(mentorlogin)        

def mentoraccept(request,id):
    booking=Booking_Details.objects.get(id=id)
    booking.slot_is_active=True
    booking.save()
    
    return redirect(mentorbooking)

def mentorbusy(request):
    user=request.user
    id=user.id
    mentor=Mentor.objects.get(mentoruser_id=id)
    mentor.is_available=False
    mentor.save()
    return redirect(mentordash)

def mentornotbusy(request):
    user=request.user
    id=user.id
    mentor=Mentor.objects.get(mentoruser_id=id)
    mentor.is_available=True
    mentor.save()    
    return redirect(mentordash)

