from django.db import models



class Slots(models.Model):
    booked_slot=models.CharField(max_length=40)


    def __str__(self):
        return self.booked_slot
  


