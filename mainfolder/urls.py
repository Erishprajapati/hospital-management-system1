"""
URL configuration for mainfolder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

def root_view(request):
    return JsonResponse({
        "message": "Welcome to Hospital Management System API",
        "endpoints": {
            "admin": {
                "url": "/admin/",
                "description": "Django admin interface"
            },
            "api": {
                "url": "/api/v1/",
                "description": "Main API endpoints",
                "available_endpoints": {
                    "patients": {
                        "list": "/api/v1/api/patients/",
                        "add": "/api/v1/add_patient"
                    },
                    "doctors": {
                        "list": "/api/v1/api/doctors/",
                        "info": "/api/v1/doctorinfo/",
                        "dashboard": "/api/v1/doctor_dashboard",
                        "shift": "/api/v1/doctor_shift"
                    },
                    "appointments": {
                        "list": "/api/v1/api/appointments",
                        "book": "/api/v1/add-appointment/",
                        "approve": "/api/v1/api/approve_appointment/<id>/"
                    },
                    "auth": {
                        "login": "/api/v1/login_view",
                        "logout": "/api/v1/logout_view",
                        "register": "/api/v1/register_view"
                    }
                }
            },
            "documentation": {
                "swagger": "/api/v1/swagger/",
                "redoc": "/api/v1/redoc/"
            }
        }
    })

schema_view = get_schema_view(
    openapi.Info(
        title="Hospital Management System API",
        default_version='v1',
        description="API documentation for the Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@hms.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include('codes.urls')),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ])),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
