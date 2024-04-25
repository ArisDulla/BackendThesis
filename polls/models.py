from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custome user manager."""

    def create_user(self, email, username, password=None, **extra_kwargs):
        """Create and saves a User with the given email, username and password."""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_kwargs):
        """Create and saves a superuser with the given email,username and password."""

        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=False
    )
    phone_number = models.ForeignKey(
        PhoneNumber, on_delete=models.SET_NULL, null=True, blank=False
    )
    """Custom user model representing user in the system."""
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """Return string representation of the object."""
        return self.email

    def has_perm(self, perm, obj=None):
        """Check if the user have a specific permission."""
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        """Check if the user have permissions to view the app `app_label."""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Check if the user a member of staff."""
        # Simplest possible answer: All admins are staff
        return self.is_admin


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


class Passport(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=False)
    place_of_birth = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    passport_number = models.CharField(max_length=100, unique=True)

    issuing_authority = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True
    )

    date_of_issue = models.DateField(null=False)
    date_of_expiry = models.DateField(null=False)

    passport_application = models.ForeignKey(
        PassportApplication, on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    submitted_at = models.DateTimeField(auto_now_add=True)
