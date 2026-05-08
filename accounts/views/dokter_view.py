from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import User, Dokter
from django.urls import reverse

from ..services.dokter_service import DokterService
from ..forms import DokterForm

@login_required
def dokter_index(request):
    users = User.objects.filter(role='dokter').order_by('-id')
    context = {
        'users': users,
        'breadcrumbs': [
            {'name': 'Manajemen Dokter', 'url': reverse('dokter_index')},
        ],
        'page_title': 'Manajemen Dokter'
    }
    return render(request, 'pages/accounts/dokter/index.html', context)

@login_required
def dokter_create(request):
    form = DokterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            user_data = {k: data[k] for k in ['username', 'full_name', 'email', 'password']}
            dokter_data = {k: data[k] for k in ['spesialisasi', 'nomor_sip', 'tarif_jasa', 'alamat', 'no_hp']}
            DokterService.create_dokter(user_data, dokter_data)
            messages.success(request, f"Dokter {data['full_name']} berhasil didaftarkan.")
            return redirect('dokter_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    context = {
        'form': form,
        'breadcrumbs': [
            {'name': 'Manajemen Dokter', 'url': reverse('dokter_index')},
            {'name': 'Registrasi Dokter', 'url': None},
        ],
        'page_title': 'Tambah Dokter Baru'
    }
    return render(request, 'pages/accounts/dokter/create.html', context)

@login_required
def dokter_edit(request, id):
    try:
        dokter = Dokter.objects.get(id=id)
    except Dokter.DoesNotExist:
        messages.error(request, "Dokter tidak ditemukan.")
        return redirect('dokter_index', role_type='dokter')

    initial_data = {
        'username': dokter.user.username,
        'full_name': dokter.user.full_name,
        'email': dokter.user.email,
        'spesialisasi': dokter.spesialisasi,
        'nomor_sip': dokter.nomor_sip,
        'tarif_jasa': dokter.tarif_jasa,
        'alamat': dokter.alamat,
        'no_hp': dokter.no_hp,
    }

    form = DokterForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        try:
            data = form.cleaned_data
            user_data = {k: data[k] for k in ['username', 'full_name', 'email', 'password']}
            dokter_data = {k: data[k] for k in ['spesialisasi', 'nomor_sip', 'tarif_jasa', 'alamat', 'no_hp']}
            DokterService.update_dokter(id, user_data, dokter_data)
            messages.success(request, f"Data dokter {data['full_name']} berhasil diupdate.")
            return redirect('dokter_index')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    context = {
        'form': form,
        'dokter': dokter,
        'page_title': 'Edit Dokter',
        'breadcrumbs': [
            {'name': 'Manajemen Dokter', 'url': reverse('dokter_index')},
            {'name': 'Edit Dokter', 'url': None},
        ],
    }
    return render(request, 'pages/accounts/dokter/edit.html', context)

@login_required
def dokter_delete(request, id):
    try:
        DokterService.delete_dokter(id)
        messages.success(request, "Data dokter dan akun user berhasil dihapus.")
    except Dokter.DoesNotExist:
        messages.error(request, "Dokter tidak ditemukan.")
    except Exception as e:
        messages.error(request, f"Terjadi kesalahan: {str(e)}")
            
    return redirect('dokter_index')
