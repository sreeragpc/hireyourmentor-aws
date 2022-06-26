from django.urls import path
from . import views

urlpatterns = [
     path('', views.adminlogin, name='adminlogin'),
     path('adminhome', views.adminhome, name='adminhome'),
     path('adminlogout',views.adminlogout, name='adminlogout'),
     path('adminmentor',views.adminmentor, name='adminmentor'),
     path('adminbooking',views.adminbooking, name='adminbooking'),
     path('adminblock/<int:id>', views.adminblock, name='adminblock'), 
     path('adminunblock/<int:id>', views.adminunblock, name='adminunblock'), 
     path('mentorblock/<int:id>', views.mentorblock, name='mentorblock'), 
     path('mentorunblock/<int:id>', views.mentorunblock, name='mentorunblock'),
]
