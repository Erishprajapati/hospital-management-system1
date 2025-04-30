from django import forms
from .models import *
from datetime import date

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


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dateofbirth', 'gender', 'phone', 'email', 'password', 'address']
        widgets = {
            'password' : forms.PasswordInput()
        }

    def clean_dateofbirth(self):
        dob = self.cleaned_data['dateofbirth']
        today = date.today()
        age_in_years = (today - dob).days / 365.25

        if age_in_years < 2:
            raise forms.ValidationError("Patient must be at least 2 years old.")
        return dob


