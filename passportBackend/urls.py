"""
URL configuration for passportBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from polls.viewsAll.v1_AddressViewSet import AddressViewSet
from polls.viewsAll.v2_PhoneNumberViewSet import PhoneNumberViewSet
from polls.viewsAll.v3_DepartmentViewSet import DepartmentViewSet
from polls.viewsAll.v4_CustomUserViewSet import CustomUserViewSet
from polls.viewsAll.v5_EmployeeViewSet import EmployeeViewSet
from polls.viewsAll.v6_CityzensViewSet import CityzensViewSet


router = DefaultRouter()
router.register(r"address", AddressViewSet, basename="user")
router.register(r"phoneNumber", PhoneNumberViewSet, basename="user")
router.register(r"departments", DepartmentViewSet, basename="user")
router.register(r"users", CustomUserViewSet, basename="user")
router.register(r"employees", EmployeeViewSet, basename="user")
router.register(r"cityzens", CityzensViewSet, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
