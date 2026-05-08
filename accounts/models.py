from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, full_name, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, username=username, email=email, **extra_fields)
        
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(full_name, username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('dokter', 'Dokter'),
        ('pasien', 'Pasien'),
    )

    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pasien')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class Dokter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dokter_profile')
    spesialisasi = models.CharField(max_length=100)
    nomor_sip = models.CharField(max_length=50)
    tarif_jasa = models.DecimalField(max_digits=12, decimal_places=2)
    no_hp = models.CharField(max_length=5)
    alamat = models.TextField()

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    jabatan = models.CharField(max_length=50)
    shift_kerja = models.CharField(max_length=50)
    no_hp = models.CharField(max_length=5)
    alamat = models.TextField()

class Pasien(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pasien_profile')
    nomor_rekam_medis = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    alamat = models.TextField()
    no_hp = models.CharField(max_length=15)

