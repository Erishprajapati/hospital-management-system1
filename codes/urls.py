from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('add_patient', views.add_patient, name = "add_patient"),
    path('success/', views.success_page, name = "success_page"),
    path('doctorinfo/', views.view_doctor, name = 'doctor_info'),
    path('api/patients/', views.list_patient_api, name='patient_list_api'),
    path('api/doctors/', views.list_doctor_api, name='list_doctors_api'),
    path('add-appointment/', views.book_appointment, name='appointment_form'),
    path('api/appointments', views.appointment_api, name = 'appointment_api'),
    path('api/approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    # path('patient_login', views.patient_login, name = 'patient_login'),
    # path('doctor_login', views.doctor_login, name = 'doctor_login'),
    path('doctor_dashboard', views.doctor_dashboard, name = 'doctor_dashboard'),
    path('patient_dashboard', views.patient_dashboard, name = 'patient_dashboard'),
    path('login_view', views.login_view, name = "login_view"),
    path('logout_view', views.logout_view, name ='logout_view'),
    path('register_view', views.patient_register, name = 'patient_register')
]