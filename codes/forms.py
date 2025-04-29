from django import forms
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'reason_for_visit', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['appointment_time'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['patient'].widget.attrs['readonly'] = True
