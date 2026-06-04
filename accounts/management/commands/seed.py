from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from accounts.models import User, Dokter, Staff, Pasien
from keuangan.models import MetodePembayaran
from pelayanan.models import TindakanMedis, Kunjungan, RekamMedis, TindakanRekamMedis
from farmasi.models import KategoriObat, Obat, Resep, DetailResep
from keuangan.models import Tagihan
from administrasi.models import Loket, Poli, JadwalPraktik


class Command(BaseCommand):
    help = 'Seed database dengan data testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum seed',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_database()

        self.stdout.write(self.style.SUCCESS('🌱 Mulai seeding database...'))
        
        # Seed data
        self.seed_users()
        self.seed_poli()
        self.seed_tindakan_medis()
        self.seed_metode_pembayaran()
        self.seed_jadwal_praktik()
        self.seed_kategori_obat()
        self.seed_obat()
        self.seed_loket()

        self.stdout.write(self.style.SUCCESS('✅ Database seeding selesai!'))

    def clear_database(self):
        self.stdout.write(self.style.WARNING('🗑️ Menghapus data lama...'))
        models = [
            Loket, Tagihan, DetailResep, Resep, Obat, KategoriObat,
            TindakanRekamMedis, RekamMedis, Kunjungan, JadwalPraktik,
            MetodePembayaran, TindakanMedis, Poli, Dokter, Staff, Pasien, User
        ]
        for model in models:
            model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Data lama berhasil dihapus'))

    def seed_users(self):
        self.stdout.write('📝 Membuat User...')
        
        # Admin
        admin = User.objects.create_user(
            full_name='Superadmin',
            username='superadmin',
            email='admin@simk.com',
            password='password',
            role="admin"
        )
        
        # Dokter
        dokter_user = User.objects.create_user(
            full_name='Dr. Budi Santoso',
            username='dokter_budi',
            email='budi@simk.com',
            password='password',
            role='dokter'
        )
        
        Dokter.objects.create(
            user=dokter_user,
            spesialisasi='Umum',
            nomor_sip='12345/2020',
            tarif_jasa=Decimal('150000.00'),
            no_hp='081234567890',
            alamat='Jl. Merdeka No. 10'
        )
        
        # Dokter 2
        dokter_user2 = User.objects.create_user(
            full_name='Dr. Siti Nurhaliza',
            username='dokter_siti',
            email='siti@simk.com',
            password='dokter123',
            role='dokter'
        )
        
        Dokter.objects.create(
            user=dokter_user2,
            spesialisasi='Gigi',
            nomor_sip='54321/2020',
            tarif_jasa=Decimal('200000.00'),
            no_hp='081234567891',
            alamat='Jl. Sudirman No. 20'
        )
        
        # Staff - Administrasi
        staff_user = User.objects.create_user(
            full_name='Rina Wijaya',
            username='staff_rina',
            email='rina@simk.com',
            password='password',
            role='staff',
        )
        
        Staff.objects.create(
            user=staff_user,
            jabatan='Administrasi',
            shift_kerja='Pagi',
            no_hp='082345678901',
            alamat='Jl. Gatot Subroto No. 5'
        )
        
        # Staff - Kasir
        staff_user2 = User.objects.create_user(
            full_name='Hendra Gunawan',
            username='staff_hendra',
            email='hendra@simk.com',
            password='password',
            role='staff',
        )
        
        Staff.objects.create(
            user=staff_user2,
            jabatan='Kasir',
            shift_kerja='Siang',
            no_hp='082345678902',
            alamat='Jl. Ahmad Yani No. 15'
        )
        
        # Staff - Apoteker
        staff_user3 = User.objects.create_user(
            full_name='Diana Putri',
            username='staff_diana',
            email='diana@simk.com',
            password='password',
            role='staff',
        )
        
        Staff.objects.create(
            user=staff_user3,
            jabatan='Apoteker',
            shift_kerja='Pagi',
            no_hp='082345678903',
            alamat='Jl. Diponegoro No. 25'
        )
        
        # Pasien
        pasien_user = User.objects.create_user(
            full_name='Bambang Sutrisno',
            username='pasien_bambang',
            email='bambang@simk.com',
            password='password',
            role='pasien'
        )
        
        Pasien.objects.create(
            user=pasien_user,
            nik='3213140589900001',
            tanggal_lahir=datetime(1990, 9, 5).date(),
            jenis_kelamin='L',
            alamat='Jl. Kemerdekaan No. 100',
            no_hp='083456789012'
        )
        
        # Pasien 2
        pasien_user2 = User.objects.create_user(
            full_name='Siti Nurhaliza',
            username='pasien_siti',
            email='sitiharsha@simk.com',
            password='pasien123',
            role='pasien'
        )
        
        Pasien.objects.create(
            user=pasien_user2,
            nik='3213140592850002',
            tanggal_lahir=datetime(1985, 3, 12).date(),
            jenis_kelamin='P',
            alamat='Jl. Merdeka No. 50',
            no_hp='083456789013'
        )
        
        self.stdout.write(self.style.SUCCESS('✓ User berhasil dibuat'))

    def seed_poli(self):
        self.stdout.write('🏥 Membuat Poli...')
        
        poli_data = [
            ('U', 'Poli Umum'),
            ('G', 'Poli Gigi'),
            ('K', 'Poli KIA'),
            ('T', 'Poli TB'),
        ]
        
        for kode, nama in poli_data:
            Poli.objects.create(kode_poli=kode, nama_poli=nama)
        
        self.stdout.write(self.style.SUCCESS('✓ Poli berhasil dibuat'))

    def seed_tindakan_medis(self):
        self.stdout.write('💉 Membuat Tindakan Medis...')
        
        tindakan_data = [
            ('Pemeriksaan Umum', Decimal('50000.00')),
            ('Injeksi', Decimal('75000.00')),
            ('Perawatan Gigi', Decimal('150000.00')),
            ('Pembersihan Gigi', Decimal('100000.00')),
            ('Pemeriksaan TB', Decimal('200000.00')),
        ]
        
        for nama, tarif in tindakan_data:
            TindakanMedis.objects.create(nama_tindakan=nama, tarif=tarif)
        
        self.stdout.write(self.style.SUCCESS('✓ Tindakan Medis berhasil dibuat'))

    def seed_metode_pembayaran(self):
        self.stdout.write('💳 Membuat Metode Pembayaran...')
        
        metode_data = ['Tunai', 'Debit', 'Kredit', 'Transfer']
        
        for metode in metode_data:
            MetodePembayaran.objects.create(nama_metode=metode)
        
        self.stdout.write(self.style.SUCCESS('✓ Metode Pembayaran berhasil dibuat'))

    def seed_jadwal_praktik(self):
        self.stdout.write('📅 Membuat Jadwal Praktik...')
        
        dokter_list = Dokter.objects.all()
        poli_list = Poli.objects.all()
        
        hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        
        for i, dokter in enumerate(dokter_list):
            poli = poli_list[i % len(poli_list)]
            for j, hari in enumerate(hari_list):
                JadwalPraktik.objects.create(
                    dokter=dokter,
                    poli=poli,
                    hari=hari,
                    jam_mulai=timezone.now().replace(hour=8, minute=0).time(),
                    jam_selesai=timezone.now().replace(hour=12, minute=0).time()
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Jadwal Praktik berhasil dibuat'))

    def seed_kategori_obat(self):
        self.stdout.write('💊 Membuat Kategori Obat...')
        
        kategori_data = ['Analgesik', 'Antibiotik', 'Antiinflamasi', 'Vitamin']
        
        for nama in kategori_data:
            KategoriObat.objects.create(nama_kategori=nama)
        
        self.stdout.write(self.style.SUCCESS('✓ Kategori Obat berhasil dibuat'))

    def seed_obat(self):
        self.stdout.write('💊 Membuat Obat...')
        
        kategori_list = KategoriObat.objects.all()
        
        obat_data = [
            ('Paracetamol', 0, 'Tablet', 100, Decimal('2500.00')),
            ('Amoxicillin', 1, 'Kaplet', 50, Decimal('5000.00')),
            ('Ibuprofen', 2, 'Tablet', 75, Decimal('3500.00')),
            ('Vitamin C', 3, 'Tablet', 200, Decimal('1500.00')),
            ('Metronidazole', 1, 'Tablet', 60, Decimal('4000.00')),
        ]
        
        for nama, kategori_idx, satuan, stok, harga in obat_data:
            Obat.objects.create(
                nama_obat=nama,
                kategori=kategori_list[kategori_idx],
                satuan=satuan,
                stok=stok,
                harga_jual=harga
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Obat berhasil dibuat'))

    def seed_loket(self):
        self.stdout.write('🪟 Membuat Loket...')
        
        staff_list = Staff.objects.filter(jabatan__in=['Administrasi'])
        kunjungan = Kunjungan.objects.first()
        
        for i, staff in enumerate(staff_list):
            Loket.objects.create(
                nama_loket=f'Loket {i+1}',
                staff=staff,
                kunjungan=kunjungan if i == 0 else None
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Loket berhasil dibuat'))
