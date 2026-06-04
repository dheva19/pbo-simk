from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from datetime import datetime

class TimestampModel(models.Model):
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, full_name, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, username=username, email=email, **extra_fields)
        
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('dokter', 'Dokter'),
        ('pasien', 'Pasien'),
    )

    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pasien')

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

class UserProfileModel(TimestampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='%(class)s_profile' 
    )
    no_hp = models.CharField(max_length=15)
    alamat = models.TextField()

    class Meta:
        abstract = True 

    def get_identitas(self):
        raise NotImplementedError(f"{self.__class__.__name__} harus implement _get_identitas()")
    
    def _format_no_hp(self):
        if self.no_hp.startswith('0'):
            self.no_hp = '+62' + self.no_hp[1:]

    def save(self, *args, **kwargs):
        self._format_no_hp()
        super().save(*args, **kwargs)

class Dokter(UserProfileModel):
    spesialisasi = models.CharField(max_length=100)
    nomor_sip = models.CharField(max_length=50)
    tarif_jasa = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'dokter'

    def get_identitas(self):
        return f"{self.user.full_name} (Dokter {self.spesialisasi})"
    
class Staff(UserProfileModel):
    jabatan = models.CharField(max_length=50)
    shift_kerja = models.CharField(max_length=50)

    class Meta:
        db_table = 'staff'

    def get_identitas(self):
        return f"{self.user.full_name} ({self.jabatan})"
    
class Pasien(UserProfileModel):
    nomor_rekam_medis = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])

    class Meta:
        db_table = 'pasien'

    def get_identitas(self):
        return f"{self.nomor_rekam_medis} - {self.user.full_name}"
    
    @property
    def umur(self):
        import datetime
        today = datetime.date.today()
        return today.year - self.tanggal_lahir.year - (
            (today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day)
        )

    def save(self, *args, **kwargs):
        if not self.nomor_rekam_medis:
            self.nomor_rekam_medis = self.__generate_nomor_rm()
        
        super().save(*args, **kwargs)

    def __generate_nomor_rm(self):
        today_str = datetime.now().strftime('%Y%m%d')
        prefix = f"RM-{today_str}-"
        
        last_pasien = Pasien.objects.filter(
            nomor_rekam_medis__startswith=prefix
        ).order_by('-nomor_rekam_medis').first()
        
        if last_pasien:
            last_number = int(last_pasien.nomor_rekam_medis.split('-')[-1])
            new_number = str(last_number + 1).zfill(3)
        else:
            new_number = "001"
            
        return f"{prefix}{new_number}"

