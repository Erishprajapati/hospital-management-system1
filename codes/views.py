from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import *
from .forms import PatientForm, DoctorForm, PatientRegistrationForm, AppointmentForm
from .serializers import (
    PatientSerializer,
    PublicDoctorSerializer,
    FullDoctorSerializer,
    AppointmentSerializer,
    BillingSerializer,
)

def home(request):
    if request.session.get('patient_id'):
        return redirect('login_view')
    elif request.session.get('doctor_id'):
        return redirect('login_view')
    else:
        return redirect('login_view')

def success_page(request):
    return render(request, 'success.html')

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            # Check for existing email or phone number
            if Patient.objects.filter(email=email).exists():
                messages.error(request, 'A patient with this email already exists.')
            elif Patient.objects.filter(phone=phone).exists():
                messages.error(request, 'A patient with this phone number already exists.')
            else:
                form.save()
                return redirect('success_page')
    else:
        form = PatientForm()
        
    return render(request, 'add_patient.html', {'form': form})

def doctor_info(request):
    return render(request, 'doctorinfo.html')

def view_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor added successfully!")
            return redirect('doctor_info')
    else:
        form = DoctorForm()
    return render(request, 'doctorinfo.html', {'form': form})

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all patients",
    responses={200: PatientSerializer(many=True)}
)
@api_view(['GET'])
def list_patient_api(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all doctors. Superusers receive full details; others receive public information.",
    responses={200: openapi.Response('Doctor data', schema=PublicDoctorSerializer(many=True))}
)
@api_view(['GET'])
def list_doctor_api(request):
    doctors = Doctor.objects.all()
    if request.user.is_superuser:
        serializer = FullDoctorSerializer(doctors, many=True)
    else:
        serializer = PublicDoctorSerializer(doctors, many=True)
    return Response(serializer.data)

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            messages.success(request, "Registration successful!")
            return redirect('patient_dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'patient_register.html', {'form': form})

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all appointments",
    responses={200: AppointmentSerializer(many=True)}
)
@swagger_auto_schema(
    method='post',
    operation_description="Create a new appointment",
    request_body=AppointmentSerializer,
    responses={201: AppointmentSerializer}
)
@api_view(['GET', 'POST'])
def appointment_api(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='patch',
    operation_description="Approve an appointment by ID. Only the assigned doctor can approve.",
    responses={
        200: openapi.Response(description="Appointment approved successfully"),
        403: openapi.Response(description="Not authorized to approve this appointment"),
        404: openapi.Response(description="Appointment not found"),
    }
)
@api_view(["PATCH"])
def approve_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
    if appointment.doctor.id != request.user.id:
        return Response({'error': 'You are not authorized to approve this appointment'}, status=status.HTTP_403_FORBIDDEN)
    appointment.is_approved = True
    appointment.save()
    return Response({'message': 'Appointment approved successfully'}, status=status.HTTP_200_OK)

@login_required
def book_appointment(request):
    if request.method == "POST":
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found.")
            return redirect('patient_dashboard')

        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        doctor_id = request.POST.get('doctor')
        reason = request.POST.get('reason_for_visit')
        notes = request.POST.get('notes')

        try:
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please select a valid date.")
            return render(request, 'add_appointment.html')

        if appointment_date < datetime.now().date():
            messages.error(request, "You cannot select a past date for the appointment.")
            return render(request, 'add_appointment.html')

        Appointment.objects.create(
            patient=patient,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason_for_visit=reason,
            notes=notes
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('patient_dashboard')
    else:
        form = AppointmentForm(initial={'patient': request.user.id})
        return render(request, 'add_appointment.html', {'form': form})

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all billing records",
    responses={200: BillingSerializer(many=True)}
)
@api_view(['GET'])
def billing_api(request):
    billing = Billing.objects.all()
    serializer = BillingSerializer(billing, many=True)
    return Response(serializer.data)

def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('login_view')
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_dashboard.html', {'doctor': doctor})

@login_required
def doctor_shift(request):
    if request.method == "POST":
        available_date = request.POST.get("appointment_date")
        available_time_start = request.POST.get("appointment_time_start")
        available_time_end = request.POST.get("appointment_time_end")

        try:
            doctor = get_object_or_404(Doctor, user=request.user)
            doctor.available_date = available_date
            doctor.available_time_start = available_time_start
            doctor.available_time_end = available_time_end
            doctor.save()
            messages.success(request, "Shift has been updated")
            return redirect('doctor_dashboard')
        except Exception as e:
            print("Error:", e)
            messages.error(request, "Unable to update shift! Try later")
            return redirect('doctor_shift')
    return render(request, 'doctor_shift.html')

@login_required
def patient_dashboard(request):
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found.")
        return redirect('home')

    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
    return render(request, 'patient_dashboard.html', {'appointments': appointments})

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
                    return redirect('patient_dashboard')
                else:
                    messages.error(request, "Incorrect patient credentials")
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found")
        elif user_type == 'doctor':
            try:
                doctor = Doctor.objects.get(email=email)
                if doctor.password == password:
                    request.session['doctor_id'] = doctor.id
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, "Incorrect doctor credentials")
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor not found")
    return render(request, 'login.html')
