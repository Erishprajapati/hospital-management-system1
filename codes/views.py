from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages


def success_page(request):
    return render(request, 'success.html')  # Renders success.html page

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = PatientForm()  # For GET request, create empty form
    
    return render(request, 'add_patient.html', {'form': form})

def doctor_info(request):
    return render(request, 'doctorinfo.html')

def view_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor added successfully!")  # ✅ Add message
            return redirect('doctor_info')  # Redirect to clear the form after submit
    else:
        form = DoctorForm()
    
    return render(request, 'doctorinfo.html', {'form': form})
