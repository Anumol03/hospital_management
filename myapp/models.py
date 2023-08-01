from django.db import models

from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    qualification = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status_choices = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    def __str__(self):
        return f"{self.name} - {self.date} {self.time_slot}"