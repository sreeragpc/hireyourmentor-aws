from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('mentordash', views.mentordash, name='mentordash'),
     path('mentorsignup', views.mentorsignup, name='mentorsignup'),
     path('mentorlogin', views.mentorlogin, name='mentorlogin'),
     path('mentorotp', views.mentorotp, name='mentorotp'),
     path('mentoredit', views.mentoredit, name='mentoredit'),
     path('mentorlogout', views.mentorlogout, name='mentorlogout'),
     path('mentorbooking', views.mentorbooking, name='mentorbooking'),
     path('mentorpassword', views.mentorpassword, name='mentorpassword'), 
     path('mentoraccept/<int:id>', views.mentoraccept, name='mentoraccept'), 
     path('mentorbusy', views.mentorbusy, name='mentorbusy'),
     path('mentornotbusy', views.mentornotbusy, name='mentornotbusy'),  
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)