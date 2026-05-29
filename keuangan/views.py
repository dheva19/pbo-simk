from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tagihan
from pelayanan.models import Kunjungan 
from django.urls import reverse

@login_required
def keuangan_tagihan_index(request):
    data_kunjungan = Kunjungan.objects.filter(status='selesai')
    context = {
        'data_kunjungan': data_kunjungan,
        'breadcrumbs': [
            {'name': 'Tagihan Pasien', 'url': reverse('keuangan_tagihan_index')},
        ],
        'page_title': 'Tagihan Pasien'
    }
    return render(request, 'pages/keuangan/tagihan_pasien/index.html', context)
