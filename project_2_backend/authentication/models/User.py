from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    # handling the common logic for creating an user
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # for creating a regular user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    # for craeting a superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

# Our custom user
class User(AbstractBaseUser, PermissionsMixin):
    # file will be uploaded to MEDIA_ROOT/user_<user_id>/<filename>
    def user_image_path(instance, filename):
        return f'user_{instance.id}/{filename}'
    # difining the user fields
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # specifies that the eamil will be used in authentication instade of the username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # set the custmUserManager as the manger of this model instade of the default one
    objects = CustomUserManager()
    # used to show the email when printing an instance of that model
    def __str__(self):
        return self.email