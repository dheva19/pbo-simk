from django.db import transaction
from ..models import User, Dokter

class DokterService:
    @staticmethod
    @transaction.atomic
    def create_dokter(user_data, dokter_data):
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            full_name=user_data['full_name'],
            role='dokter'
        )
        
        dokter = Dokter.objects.create(
            user=user,
            **dokter_data
        )
        
        return dokter
    
    @staticmethod
    @transaction.atomic
    def update_dokter(dokter_id, user_data, dokter_data):
        dokter = Dokter.objects.get(id=dokter_id)
        user = dokter.user

        user.username = user_data.get('username', user.username)
        user.full_name = user_data.get('full_name', user.full_name)
        user.email = user_data.get('email', user.email)
        
        password = user_data.get('password')
        if password and password.strip():
            user.set_password(password)
        
        user.save()

        for attr, value in dokter_data.items():
            setattr(dokter, attr, value)
        
        dokter.save()
        return dokter
    
    @staticmethod
    @transaction.atomic
    def delete_dokter(dokter_id):
        dokter = Dokter.objects.get(id=dokter_id)
        
        user = dokter.user
        user.delete() 
        
        return True