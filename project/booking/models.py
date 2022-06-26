from django.db import models
from slots.models import Slots
from user.models import User
from mentor.models import Mentor






class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)



class Booking_Details(models.Model):
    booking= models.ForeignKey(Booking, on_delete = models.CASCADE)
    selected_mentor=models.ForeignKey(Mentor, on_delete = models.CASCADE)
    slot= models.ForeignKey(Slots, on_delete = models.CASCADE,null=True,blank=True)
    booked_date=models.DateField(null=True,blank=True)
    slot_is_active=models.BooleanField(default=False)
