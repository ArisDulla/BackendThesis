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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from polls.viewsAll.v1_AddressViewSet import AddressViewSet
from polls.viewsAll.v2_PhoneNumberViewSet import PhoneNumberViewSet
from polls.viewsAll.v3_DepartmentViewSet import DepartmentViewSet
from polls.viewsAll.v4_CustomUserViewSet import CustomUserViewSet
from polls.viewsAll.v5_EmployeeViewSet import EmployeeViewSet
from polls.viewsAll.v6_CityzensViewSet import CityzensViewSet
from polls.viewsAll.v7_PassportViewSet import PassportViewSet
from polls.viewsAll.fv0_passportApplications.v1_IssuancePassportViewSet import (
    IssuancePassportViewSet,
)
from polls.viewsAll.fv0_passportApplications.v2_RenewalPassportViewSet import (
    RenewalPassportViewSet,
)
from polls.viewsAll.fv0_passportApplications.v3_ReplacementPassportViewSet import (
    ReplacementPassportViewSet,
)
from polls.viewsAll.fv0_passportApplications.v4_TheftOrLossPassportViewSet import (
    TheftOrLossPassportViewSet,
)
from polls.viewsAll.fv0_passportApplications.v5_IssuanceMinorsPassportViewSet import (
    IssuanceMinorsPassportViewSet,
)

router = DefaultRouter()
router.register(r"address", AddressViewSet, basename="address")
router.register(r"phoneNumber", PhoneNumberViewSet, basename="phoneNumber")
router.register(r"departments", DepartmentViewSet, basename="departments")
router.register(r"users", CustomUserViewSet, basename="users")
router.register(r"employees", EmployeeViewSet, basename="employees")
router.register(r"cityzens", CityzensViewSet, basename="cityzens")
router.register(r"passportInfo", PassportViewSet, basename="passportinfo")

#
# Applications PASSPORT
#

# Issuance Passport
router.register(
    r"issuance-passport", IssuancePassportViewSet, basename="issuance-passport"
)

# Renewal Passport
router.register(
    r"renewal-passport", RenewalPassportViewSet, basename="renewal-passport"
)

# Replacement Passport
router.register(
    r"replacement-passport",
    ReplacementPassportViewSet,
    basename="replacement-passport",
)

# Theft Or Loss Passport
router.register(
    r"theftOrLoss-passport",
    TheftOrLossPassportViewSet,
    basename="theftOrLoss-passport",
)
# Issuance Minors Passport
router.register(
    r"issuanceMinors-passport",
    IssuanceMinorsPassportViewSet,
    basename="issuanceMinors-passport",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    #
    # Djoser and Simple JWT
    #
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),  # JWT’s
    path("auth/", include("djoser.urls.authtoken")),
    #
    # Social
    #
    path("auth/", include("djoser.social.urls")),
]
