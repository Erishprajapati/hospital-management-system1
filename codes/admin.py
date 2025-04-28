from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Billing)
admin.site.register(Appointment)
admin.site.register(Room)
admin.site.register(Admission)
admin.site.register(Prescription)
admin.site.register(Department)

