from multiprocessing import context
import razorpay
from django.http import HttpResponse
from django.shortcuts import render,redirect
from category.models import Category, Domains
from booking.models import Booking, Booking_Details
from mentor.models import Mentor
from .models import User
from slots.models import Slots
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages,auth
from user.otp import verify, verify_check
from project.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET
from django.views.decorators.csrf import csrf_exempt

def all_logout(request):
   try: 
        user=request.user 
        if user.user_role=='mentor' or user.user_role=='admin':
            logout(request)     
        return redirect(userlogin)
   except:
       return redirect(userhome)

def userlogin(request):
    if request.user.is_authenticated  :
        return redirect(userhome) 
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None and user.user_role=='student' and user.is_admin==False:
            login(request, user)
            return redirect(userhome)
        else:
            messages.error(request,'invalid credentials')    
    return render(request, 'userlogin.html')

def userhome(request):
    all_logout(request)
    cat=Category.objects.all()
    dom=Domains.objects.all()
    context={
        'cat':cat,
        'dom':dom,
        }
    if request.user.is_authenticated:
        return render(request, 'userhome.html',context)    
    return render(request, 'index.html',context)  

def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(userhome)       

def usersignup(request):
 logout(request)
 try:   
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            request.session['email'] = email
            city = request.POST['city']
            phone_number2 = request.POST['phone_number']
            request.session['phone_number2'] = phone_number2                
            verify(phone_number2)   
            password= request.POST['password']
            user = User.objects.create_user(first_name =first_name,last_name=last_name, username = username , email =email, city =city , phone_number = phone_number2,password = password  )
            user.user_role = "student"
            user.is_active=False
            user.save()            
            return redirect(userotp)
 except:
     messages.error(request,'Try with different email or phone number')
 return render(request, 'usersignup.html')         
    
def userotp(request):
    try:
        all_logout(request)
        phone_number=request.session['phone_number2']
        user=User.objects.get(phone_number=phone_number)
        if request.method== 'POST':
            otp=request.POST['otp']
            if verify_check(phone_number,otp)==True:
                user.is_active=True
                user.save()
                return redirect(userlogin)
            else:
                messages.error(request,'otp entered is incorrect!')
    except:
        messages.error(request,'try again!')
        return redirect(usersignup)            
    return render(request, 'userotp.html')

def userpassword(request):
     all_logout(request)
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
                return redirect('userdash')
            else:
                messages.error(request, 'give same password')
        else:
            messages.error(request, 'wrong password')
     if request.user.is_authenticated:
        return render(request,'userpassword.html')  
     return redirect(userlogin)      


def userdash(request):
    all_logout(request)
    return render(request,'userdash.html')    

def useredit(request):
    all_logout(request)
    user=request.user
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
        return redirect(userdash)   
    if request.user.is_authenticated:
        return render(request,'useredit.html')  
    return redirect(userlogin)     

def userbooking(request):
    all_logout(request)
    user=request.user
    id=user.id
    bookings=Booking_Details.objects.all()
    context={
        'bookings':bookings,
        'id':id
    } 
    if request.user.is_authenticated:
       return render(request,'userbooking.html',context)
    return redirect(userlogin)           
       
def mentorloader(request,id):
    cat=Category.objects.all()
    dom=Domains.objects.all()
    mentor=Mentor.objects.filter(Dom_id=id)
    context={
            'mentor':mentor,
            'cat':cat,
            'dom':dom,
            }
    if request.user.is_authenticated  :
        return render(request, 'userhome.html',context)    
    else:
        return render(request, 'index.html',context)

def mentordetails(request,id=None):
    mentor=Mentor.objects.get(id=id)
    mentorid=mentor.id
    request.session['mentorid'] = mentorid
    userid=mentor.mentoruser_id
    price=mentor.mentor_price
    mentoruser=User.objects.get(id=userid)
    cat=Category.objects.all()
    dom=Domains.objects.all()
    slots=Slots.objects.all()

    context={
        'slots':slots,
        'userid':userid,
        'price':price,
        'mentor':mentor,
        'mentoruser':mentoruser,
        'cat':cat,
        'dom':dom,
        }
    if request.user.is_authenticated:
       return render(request,'mentordetails.html',context)
    return redirect(userlogin)   



def booking(request,id):
    try:
        mentorid = request.session['mentorid']
        if request.method == 'POST':
            date= request.POST['date']
            slots = request.POST['slots']  
        try:
            booking= Booking.objects.get(user_id=id,is_active=True)    
        except :
            booking= Booking.objects.create(user_id=id,is_active=True)
        booking_id=booking.id 
        request.session['booking_id']=booking_id   
        try:
            booking_details = Booking_Details.objects.get(booked_date =date,slot_id=slots ,selected_mentor_id =mentorid )
            messages.error(request, 'Slot is already booked please select another slot !')
            return redirect(bookingpage)

        except :
            booking_details = Booking_Details.objects.create(booked_date =date,slot_id=slots, booking_id = booking_id , selected_mentor_id =mentorid  ) 
            return redirect(bookingpage)
    except:
        messages.error(request, 'Please select a date !')
        return redirect(bookingpage)

def bookingpage(request):
    all_logout(request)
    user=request.user
    try:
        booking= Booking.objects.get(user_id=user.id,is_active=True)    
    except :
        booking= Booking.objects.create(user_id=user.id,is_active=True)
     
    book_id=booking.id 
    bookings=Booking_Details.objects.filter(booking_id=booking.id)
    sum=0
    if booking.is_active==True:
        for x in bookings:
        
            sum=sum+x.selected_mentor.mentor_price

    tax=sum*0.18
    tax=round(tax,2)
    total=sum+tax
    total=round(total,2)
    amount=total*100
    if amount > 0 and booking.is_active==True:
        client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
        response = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})        
        context={
        'RAZOR_KEY_ID':RAZOR_KEY_ID,
        'client':client,
        'bookings':bookings,
        'book_id':book_id,
        'sum':sum,
        'tax':tax,
        'total':total,
        'response':response
        }    
    else:
         context={
             'total':total,
             'sum':sum,
             'tax':tax,

         }            
    if request.user.is_authenticated:
       return render(request,'booking.html',context)
    return redirect(userlogin)     

@csrf_exempt
def booking_success(request,id):
    try:
        if request.method =="POST":      
            bookings=Booking.objects.get(id=id)
            bookings.is_active=False
            bookings.save()
            return render(request,'success.html')
    except :
        messages.error(request, 'payment failed , try again !')
        return redirect(bookingpage)
    return redirect(bookingpage)  

def removebooking(request,id):
    booking=Booking_Details.objects.get(id=id)
    booking.delete()    
    return redirect(bookingpage)    