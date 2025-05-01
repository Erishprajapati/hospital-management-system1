from django.db import models
from django.contrib.auth.models import User

# Create your models here.
gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown')
]
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=100)
    dateofbirth = models.DateField()
    gender = models.CharField(choices=gender_choices, max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    allergies = models.TextField(blank = True, null = True)
    medical_history = models.TextField(blank = True, null = True)

    def __str__(self):
        return f"{self.name}- {self.gender}- {self.blood_group}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    room_number = models.IntegerField()
    years_of_experience = models.IntegerField()
    available_date = models.DateField()
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()

    def __str__(self):
        return f"Dr.{self.name} - {self.specialization}"

status_choices = [
    ('P', 'Pending'),
    ('C', 'Confirmed'),
    ('CA', 'Cancelled'),
    ('CO', 'Completed'),
]
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(choices=status_choices, max_length=4, default = 'P')
    reason_for_visit = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient} has {self.appointment_date} with {self.doctor}"

class Department(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    head_of_department = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.description}"

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    prescribed_to = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication_details = models.TextField()
    instructions = models.TextField()
    date = models.DateField()

payment_status = [
    ('P', 'Pending'),
    ('PA', 'Paid'),
    ('C', 'Canceled'),
]
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_status = models.CharField(choices = payment_status, max_length=4)
    payment_date = models.DateField()
    billing_details = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.patient} has {self.payment_status}"
    

room_status = [
    ('I', 'ICU'),
    ('G', 'General'),
    ('P', 'Private'),
]
class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(choices = room_status, max_length=1)
    is_available = models.BooleanField()

    def __str__(self):
        return f"{self.room_number} is {self.is_available}"

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    admitted_on = models.DateField()
    discharge_on = models.DateField()
    reason = models.CharField(max_length=100)


    