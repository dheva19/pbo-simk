from django.db import models

from accounts.models import TimestampModel

class KategoriObat(TimestampModel):
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = 'kategori_obat'

class Obat(TimestampModel):
    nama_obat = models.CharField(max_length=255)
    kode_obat = models.CharField(max_length=10, unique=True)
    kategori = models.ForeignKey(KategoriObat, on_delete=models.CASCADE)
    satuan = models.CharField(max_length=20)
    stok = models.PositiveIntegerField()
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'obat'
    
    def __generate_kode_obat(self):
        kategori_prefix = self.kategori.nama_kategori[:3].upper()
        
        last_obat = Obat.objects.filter(
            kategori=self.kategori
        ).order_by('id').last()
        
        if last_obat and last_obat.kode_obat:
            last_number = int(last_obat.kode_obat[-3:])
            next_number = last_number + 1
        else:
            next_number = 1
        
        return f"OBT-{kategori_prefix}-{next_number:03d}"
    
    def save(self, *args, **kwargs):
        if not self.kode_obat:
            self.kode_obat = self.__generate_kode_obat()
        super().save(*args, **kwargs)

class Resep(TimestampModel):
    rekam_medis = models.ForeignKey('pelayanan.RekamMedis', on_delete=models.CASCADE)
    apoteker = models.ForeignKey('accounts.Staff', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='diproses')
    tanggal_resep = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resep'

class DetailResep(TimestampModel):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE)
    obat = models.ForeignKey(Obat, on_delete=models.CASCADE)
    jumlah_diminta = models.PositiveIntegerField()
    dosis_aturan = models.CharField(max_length=100)
    subtotal_harga = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detail_resep'