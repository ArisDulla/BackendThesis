from django.db import models
from django.contrib.auth.models import AbstractUser


class Address(models.Model):
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=50)
    region_name = models.CharField(max_length=100)
    prefecture_name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    class Meta:
        unique_together = [
            "street",
            "street_number",
            "region_name",
            "prefecture_name",
            "postal_code",
        ]


class PhoneNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("not_exist", "Not Exist"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class CustomUser(AbstractUser):
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=False
    )
    phone_number = models.ForeignKey(
        PhoneNumber, on_delete=models.SET_NULL, null=True, blank=False
    )
    pass


class Department(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=False
    )
    phone_number = models.ForeignKey(
        PhoneNumber, on_delete=models.SET_NULL, null=True, blank=False
    )
    email = models.EmailField()


class Employee(models.Model):
    EMPLOYEE_TYPES = (
        ("SEC", "Secretary"),
        ("YP01", "Employee 01"),
        ("YP02", "Employee 02"),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False
    )
    employee_id = models.CharField(max_length=100)
    employee_type = models.CharField(choices=EMPLOYEE_TYPES, null=True, blank=False)


class Cityzens(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        # Modify attributes of the related CustomUser instance
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.is_active = True
        self.user.groups.clear()
        self.user.user_permissions.clear()

        self.user.save()

        super().save(*args, **kwargs)


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


#
# PassportApplication
#
class PassportApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_card_copy = models.FileField(upload_to=user_directory_path)
    applicant_photo = models.ImageField(upload_to=user_directory_path)
    payment_receipt = models.FileField(upload_to=user_directory_path)

    departmentx = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False
    )

    status_choices = [
        ("pending", "Pending"),
        ("first_approval", "First Approval"),
        ("final_approval", "Final Approval"),
        ("rejected", "Rejected"),
        ("cancelated", "Cancelated"),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="pending")

    first_approval_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="first_approvals",
        null=True,
        blank=True,
    )
    final_approval_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name="final_approvals",
        null=True,
        blank=True,
    )
    rejected_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejections",
    )

    submitted_at = models.DateTimeField(auto_now_add=True)


#
# Issuance Passport
#
class IssuancePassportApplication(PassportApplication):
    #
    # (( The same documents are submitted, as in case 1  Passport Application ))
    #
    application_form = models.FileField(upload_to=user_directory_path)


#
#  Renewal Passport
#
class RenewalPassportApplication(PassportApplication):
    #
    # (( The same documents are submitted, as in case 1  Passport Application ))
    #
    old_passport_pdf = models.FileField(upload_to=user_directory_path)


#
# Replacement Passport
#
class ReplacementPassportApplication(PassportApplication):
    #
    # (( The same documents are submitted, as in case 1  Passport Application ))
    #
    old_passport_pdf = models.FileField(upload_to=user_directory_path)


#
# Theft Or Loss Passport
#
class TheftOrLossPassportApplication(PassportApplication):
    #
    # (( The same documents are submitted, as in case 1  Passport Application ))
    #
    police_report = models.FileField(upload_to=user_directory_path)


#
# Issuance Passport for minors
#
class IssuanceMinorsPassportApplication(PassportApplication):
    #
    # (( The same documents are submitted, as in case 1  Passport Application ))
    #
    caregiver_address_certification = models.FileField(upload_to=user_directory_path)
    convicted_declaration = models.FileField(upload_to=user_directory_path)
    minor_age_declaration = models.FileField(upload_to=user_directory_path)
