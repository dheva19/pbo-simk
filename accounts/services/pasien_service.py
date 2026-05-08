from django.db import transaction
from datetime import datetime
from ..models import User, Pasien

class PasienService:
    @staticmethod
    def generate_nomor_rm():
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

    @staticmethod
    @transaction.atomic
    def create_pasien(user_data, pasien_data):
        nomor_rm = PasienService.generate_nomor_rm()
        
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            full_name=user_data['full_name'],
            role='pasien'
        )
        
        pasien = Pasien.objects.create(
            user=user,
            nomor_rekam_medis=nomor_rm,
            **pasien_data
        )
        
        return pasien
    
    @staticmethod
    @transaction.atomic
    def update_pasien(pasien_id, user_data, pasien_data):
        pasien = Pasien.objects.get(id=pasien_id)
        user = pasien.user

        user.username = user_data.get('username', user.username)
        user.full_name = user_data.get('full_name', user.full_name)
        user.email = user_data.get('email', user.email)
        
        password = user_data.get('password')
        if password and password.strip():
            user.set_password(password)
        
        user.save()

        for attr, value in pasien_data.items():
            setattr(pasien, attr, value)
        
        pasien.save()
        return pasien
    
    @staticmethod
    @transaction.atomic
    def delete_pasien(pasien_id):
        pasien = Pasien.objects.get(id=pasien_id)
        
        user = pasien.user
        user.delete() 
        
        return True