from django import forms
from .models import *
from datetime import date
from django.core.exceptions import ValidationError
import re


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


# Custom validator for phone number
def validate_nepali_phone(value):
    if not re.match(r'^98\d{8}$', value):
        raise ValidationError('Phone number must start with 98 and be exactly 10 digits long.')

class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'dateofbirth', 'gender', 'phone', 'email', 'password', 'address']
        widgets = {
            'password': forms.PasswordInput(),
        }

    # Date of birth validation (Patient must be at least 2 years old)
    def clean_dateofbirth(self):
        dob = self.cleaned_data['dateofbirth']
        today = date.today()
        age_in_years = (today - dob).days / 365.25

        if age_in_years < 2:
            raise forms.ValidationError("Patient must be at least 2 years old.")
        return dob

    # Phone number validation (Must start with 98 and be 10 digits)
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        validate_nepali_phone(phone)  # Apply custom phone validation
        return phone
