# pelayanan/views/resep_obat_view
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pelayanan.models import (
    Kunjungan,
    RekamMedis,
)

from farmasi.models import (
    Obat,
    Resep,
    DetailResep
)


@login_required
def resep_obat_index(request, kunjungan_id):

    kunjungan = get_object_or_404(
        Kunjungan.objects.select_related(
            'pasien__user',
            'jadwal__dokter__user',
            'jadwal__poli'
        ),
        id=kunjungan_id
    )

    rekam_medis = RekamMedis.objects.filter(
        kunjungan=kunjungan
    ).first()

    obat_list = Obat.objects.select_related(
        'kategori'
    ).all()

    resep_obat, created = Resep.objects.get_or_create(
        rekam_medis=rekam_medis,
        defaults={
            'status': 'diproses'
        }
    )

    if request.method == 'POST':
        obat_ids = request.POST.getlist('obat_ids')
        jumlah_list = request.POST.getlist('jumlah')
        aturan_pakai_list = request.POST.getlist('aturan_pakai')
        selected_obat = []

        for index, obat_id in enumerate(obat_ids):
            jumlah = jumlah_list[index].strip()
            aturan_pakai = aturan_pakai_list[index].strip()

            if aturan_pakai and jumlah:

                if int(jumlah) <= 0:

                    messages.error(
                        request,
                        'Jumlah obat tidak boleh 0.'
                    )

                    return redirect(
                        'resep_obat_index',
                        kunjungan_id=kunjungan.id
                    )

                selected_obat.append({
                    'obat_id': obat_id,
                    'jumlah': jumlah,
                    'aturan_pakai': aturan_pakai
                })

        if len(selected_obat) < 1:
            messages.error(
                request,
                'Minimal pilih 1 obat dan isi aturan pakai.'
            )

            return redirect(
                'resep_obat_index',
                kunjungan_id=kunjungan.id
            )

        DetailResep.objects.filter(
            resep=resep_obat
        ).delete()

        for item in selected_obat:
            obat = Obat.objects.get(
                id=item['obat_id']
            )

            DetailResep.objects.create(
                resep=resep_obat,
                obat=obat,
                jumlah_diminta=item['jumlah'],
                dosis_aturan=item['aturan_pakai'],
                subtotal_harga=(
                    int(item['jumlah']) * obat.harga_jual
                )
            )

        kunjungan.status = 'menunggu_farmasi'
        kunjungan.save()

        messages.success(
            request,
            'Resep obat berhasil dibuat.'
        )

        return redirect(
            'resep_obat_index',
            kunjungan_id=kunjungan.id
        )

    detail_resep = DetailResep.objects.filter(
        resep=resep_obat
    ).select_related(
        'obat',
        'obat__kategori'
    )

    context = {
        'page_title': 'Resep Obat',
        'kunjungan': kunjungan,
        'rekam_medis': rekam_medis,
        'obat_list': obat_list,
        'detail_resep': detail_resep,
    }

    return render(
        request,
        'pages/pelayanan/resep_obat/index.html',
        context
    )