from rest_framework import serializers
from .models import *

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

# class DoctorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = "__all__"
class PublicDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'phone', 'room_number', 'available_date']

class FullDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        models = Billing
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Prescription
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        models = Room
        fields = "__all__"

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Admission
        fields = "__all__"