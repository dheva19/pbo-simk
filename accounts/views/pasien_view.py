from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import User, Pasien
from django.urls import reverse

from ..services.pasien_service import PasienService
from ..forms import PasienForm

@login_required
def pasien_index(request):
    users = User.objects.filter(role='pasien').order_by('-id')
    context = {
        'users': users,
        'breadcrumbs': [
            {'name': 'Manajemen Pasien', 'url': reverse('pasien_index')},
        ],
        'page_title': 'Manajemen Pasien'
    }
    return render(request, 'pages/accounts/pasien/index.html', context)

@login_required
def pasien_create(request):
    form = PasienForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            user_data = {k: data[k] for k in ['username', 'full_name', 'email', 'password']}
            pasien_data = {k: data[k] for k in ['nik', 'tanggal_lahir', 'jenis_kelamin', 'alamat', 'no_hp']}
            PasienService.create_pasien(user_data, pasien_data)
            messages.success(request, f"Pasien {data['full_name']} berhasil didaftarkan.")
            return redirect('pasien_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    context = {
        'form': form,
        'breadcrumbs': [
            {'name': 'Manajemen Pasien', 'url': reverse('pasien_index')},
            {'name': 'Registrasi Pasien', 'url': None},
        ],
        'page_title': 'Tambah Pasien Baru'
    }
    return render(request, 'pages/accounts/pasien/create.html', context)

@login_required
def pasien_edit(request, id):
    try:
        pasien = Pasien.objects.get(id=id)
    except Pasien.DoesNotExist:
        messages.error(request, "Pasien tidak ditemukan.")
        return redirect('pasien_index')

    initial_data = {
        'username': pasien.user.username,
        'full_name': pasien.user.full_name,
        'email': pasien.user.email,
        'nik': pasien.nik,
        'tanggal_lahir': pasien.tanggal_lahir,
        'jenis_kelamin': pasien.jenis_kelamin,
        'alamat': pasien.alamat,
        'no_hp': pasien.no_hp,
    }

    form = PasienForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            user_data = {k: data[k] for k in ['username', 'full_name', 'email', 'password']}
            pasien_data = {k: data[k] for k in ['nik', 'tanggal_lahir', 'jenis_kelamin', 'alamat', 'no_hp']}
            PasienService.update_pasien(id, user_data, pasien_data)
            messages.success(request, f"Data pasien {data['full_name']} berhasil diupdate.")
            return redirect('pasien_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'form': form,
        'pasien': pasien,
        'page_title': 'Edit Pasien',
        'breadcrumbs': [
            {'name': 'Manajemen Pasien', 'url': reverse('pasien_index')},
            {'name': 'Edit Pasien', 'url': None},
        ],
    }
    return render(request, 'pages/accounts/pasien/edit.html', context)

@login_required
def pasien_delete(request, id):
    try:
        PasienService.delete_pasien(id)
        messages.success(request, "Data pasien dan akun user berhasil dihapus.")
    except Pasien.DoesNotExist:
        messages.error(request, "Pasien tidak ditemukan.")
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan: {str(e)}")
            
    return redirect('pasien_index')
