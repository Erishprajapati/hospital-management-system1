from django.shortcuts import render,redirect
from .models import *
from .forms import *

# Create your views here.
def add_patient(request):
    if request.method =='POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success-page')
        else: 
            form = PatientForm()
            return render(request, 'add_patient.html', {'form': form})