from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     # path('', views.home, name='home'),
     path('', views.userhome, name='userhome'),
     path('userlogin', views.userlogin, name='userlogin'),
     path('usersignup', views.usersignup, name='usersignup'),
     path('userotp', views.userotp, name='userotp'),
     path('userlogout', views.userlogout, name='userlogout'),
     path('mentordetails/<int:id>', views.mentordetails, name='mentordetails'),
     path('userpassword', views.userpassword, name='userpassword'),
     path('userdash', views.userdash, name='userdash'),
     path('useredit', views.useredit, name='useredit'),
     path('userbooking', views.userbooking, name='userbooking'),
     path('bookingpage', views.bookingpage, name='bookingpage'),
     path('booking/<int:id>', views.booking, name='booking'),
     path('mentorloader/<int:id>', views.mentorloader, name='mentorloader'),
     path('removebooking/<int:id>', views.removebooking, name='removebooking'),
     path('success/<int:id>',views.booking_success,name="booking_success"),



 

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)