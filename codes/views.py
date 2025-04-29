from django.shortcuts import render, redirect
from rest_framework.response import Response
from .models import *
from .forms import *
from django.contrib import messages
from rest_framework.decorators import api_view
from .serializers import *
# from django.contrib.auth.models import user

def home(request):
    if request.session.get('patient_id'):
        return redirect('patient_dashboard')
    elif request.session.get('doctor_id'):
        return redirect('doctor_dashboard')
    else:
        return render(request, 'home.html')

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


def patient_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        try:
            patient = Patient.objects.get(email = email)
            if patient.password == password:
                """where to redirect if the login is successful"""
                request.session['patient_id'] = patient.id
                return redirect('patient_dashboard')
            else:
                messages.error(request, "Incorrect credentials")
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found!!!")
    return render(request, 'login.html')

def doctor_login(request):
    if request.method ==  "POST":
        email =  request.POST.get('email')
        password = request.POST.get('password')
        try: 
            doctor = Doctor.objects.get(email = email)
            if doctor.password == password:
                request.session['doctor_id'] = doctor.id 
                return redirect('doctor_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except Doctor.DoesNotExist:
            messages.error(request, " Doctor not found")
    return render(request, 'login.html')

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

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'P'  # Pending
            appointment.is_approved = False
            appointment.patient = request.user.id # Assuming Patient is related to User
            appointment.save()
            messages.success(request, "Appointment request sent!")
            return redirect('success')
    else:
        form = AppointmentForm(initial={'patient': user.id})
    return render(request, 'add_appointment.html', {'form': form})


@api_view(['GET'])
def billing_api(request):
    billing = Billing.objects.all()
    serializer = BillingSerializer(billing, many = True)
    return Response(request, serializer.data)


def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')  # Redirect if not logged in

    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_dashboard.html', {'doctor': doctor})

def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')  # Redirect if not logged in

    patient = Patient.objects.get(id=patient_id)
    return render(request, 'patient_dashboard.html', {'patient': patient})

def logout_view(request):
    request.session.flush()
    return redirect('home')


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
