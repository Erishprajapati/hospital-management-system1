from django.shortcuts import render, redirect
from rest_framework.response import Response
from .models import *
from .forms import *
from django.contrib import messages
from rest_framework.decorators import api_view
from .serializers import *
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import user

def home(request):
    if request.session.get('patient_id'):
        return redirect('login_view')
    elif request.session.get('doctor_id'):
        return redirect('login_view')
    else:
        return redirect('login_view')

def success_page(request):
    return render(request, 'success.html') # Renders success.html page

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

@api_view(['GET'])
def list_patient_api(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def list_doctor_api(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many = True)
    return Response(serializer.data)

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            # patient.password = make_password(form.cleaned_data['password'])  # hash password
            patient.save()
            messages.success(request, "Registration successful!")
            return redirect('patient_dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'patient_register.html', {'form': form})

@api_view(['GET', 'POST'])
def appointment_api(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AppointmentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 200)
        return Response(serializer.errors, status = 401)
    
@api_view(["PATCH"])
def approve_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id = appointment_id)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status = 404)
    if appointment.doctor.id != request.user.id:
        return Response({'error': 'You are not authorized to approve this appointment'}, status = 403)
    appointment.is_approved = True
    appointment.save()
    return Response({'message': 'Appointment approved succesfully'})

@login_required
def book_appointment(request):
    if request.method == "POST":
        # try:
        #     patient = Patient.objects.get(user=request.user)  # Assuming OneToOneField with User
        # except Patient.DoesNotExist:
        #     messages.error(request, "Patient not found.")
        #     return redirect('patient_dashboard')

        # # Extract POST data
        
        appointment_date = request.POST.get('appointment_date')
        appointment_time_start = request.POST.get('appointment_time_start')
        doctor_id = request.POST.get('doctor')
        reason = request.POST.get('reason_for_visit')
        notes = request.POST.get('notes')
        patient = Patient.objects.get(user=request.user) 
        

        # # Validate date format
        # try:
        #     appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
        # except ValueError:
        #     messages.error(request, "Invalid date format. Please select a valid date.")
        #     return render(request, 'add_appointment.html')

        # Check for past date
        # if appointment_date < datetime.now().date():
        #     messages.error(request, "You cannot select a past date for the appointment.")
        #     return render(request, 'add_appointment.html')

        # Save appointment
        Appointment.objects.create(
            patient=patient,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time_start=appointment_time_start,
            reason_for_visit=reason,
            notes=notes
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('doctor_dashboard')

    else:
        form = AppointmentForm(initial={'patient': request.user.id})
        return render(request, 'add_appointment.html', {'form': form})

@api_view(['GET'])
def billing_api(request):
    billing = Billing.objects.all()
    serializer = BillingSerializer(billing, many = True)
    return Response(request, serializer.data)


def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('login_view')  # Redirect if not logged in
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_dashboard.html', {'doctor': doctor})

@login_required
def doctor_shift(request):
    if request.method == "POST":
        patient_id = request.POST.get('patient')
        appointment_date = request.POST.get("appointment_date")
        appointment_time_start = request.POST.get("appointment_time_start")
        appointment_time_end = request.POST.get("appointment_time_end")

        try:
            patient = Patient.objects.get(id=patient_id)
            Appointment.objects.create(
                patient=patient,
                appointment_date=appointment_date,
                appointment_time_start=appointment_time_start,
                appointment_time_end=appointment_time_end
            )
            messages.success(request, "Shift has been updated")
            return redirect('doctor_dashboard')
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found")
            return redirect('doctor_shift')

    return render(request, 'doctor_shift.html') 


def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login_view')  # Redirect if not logged in

    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient_dashboard.html', {'patient': patient})

def logout_view(request):
    request.session.flush()
    return redirect('login_view')


def login_view(request):
    if request.method == "POST":
        user_type = request.POST.get('user_type')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_type == 'patient':
            try:
                patient = Patient.objects.get(email=email)
                if patient.password == password:
                    request.session['patient_id'] = patient.id
                    return redirect('patient_dashboard')  # Redirect to patient dashboard
                else:
                    messages.error(request, "Incorrect patient credentials")
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found")

        elif user_type == 'doctor':
            try:
                doctor = Doctor.objects.get(email=email)
                if doctor.password == password:
                    request.session['doctor_id'] = doctor.id
                    return redirect('doctor_dashboard')  # Redirect to doctor dashboard
                else:
                    messages.error(request, "Incorrect doctor credentials")
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor not found")

    return render(request, 'login.html')

