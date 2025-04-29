from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('add_patient', views.add_patient, name = "add_patient"),
    path('success/', views.success_page, name = "success_page"),
    path('doctorinfo/', views.view_doctor, name = 'doctor_info'),
    path('patients/', views.list_patients, name='patient_list'),
    path('doctors/', views.list_doctors, name = "doctors_list"),
    path('patient_login', views.patient_login, name = 'patient_login'),
    path('doctor_login', views.doctor_login, name = 'doctor_login')

]
