from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages


def home(request):
    return render(redirect, 'home.html')
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

def list_patients(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

def list_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors_list.html', {'doctors': doctors})


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


# def doctor_login(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         try: 
#             doctor = Doctor.objects.get(email=email)
#             if doctor.password == password:
#                 request.session['doctor_id'] = doctor.id  # fixed key name too
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid credentials')
#         except Doctor.DoesNotExist:
#             messages.error(request, "Doctor not found")
#     return render(request, 'login.html')

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
