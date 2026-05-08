from django.db import transaction
from ..models import User, Staff

class StaffService:
    @staticmethod
    @transaction.atomic
    def create_staff(user_data, staff_data):
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            full_name=user_data['full_name'],
            role='staff'
        )
        
        staff = Staff.objects.create(
            user=user,
            **staff_data
        )
        
        return staff
    
    @staticmethod
    @transaction.atomic
    def update_staff(staff_id, user_data, staff_data):
        staff = Staff.objects.get(id=staff_id)
        user = staff.user

        user.username = user_data.get('username', user.username)
        user.full_name = user_data.get('full_name', user.full_name)
        user.email = user_data.get('email', user.email)
        
        password = user_data.get('password')
        if password and password.strip():
            user.set_password(password)
        
        user.save()

        for attr, value in staff_data.items():
            setattr(staff, attr, value)
        
        staff.save()
        return staff
    
    @staticmethod
    @transaction.atomic
    def delete_staff(staff_id):
        staff = Staff.objects.get(id=staff_id)
        
        user = staff.user
        user.delete() 
        
        return True