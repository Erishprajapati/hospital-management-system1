from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('add_patient', views.add_patient, name = "add_patient"),
    path('success/', views.success_page, name = "success_page"),
    path('doctorinfo/', views.view_doctor, name = 'doctor_info')
]
