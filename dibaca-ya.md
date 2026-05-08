# Ijin Yapping Bentar

abis migrate kalau gaada akun superadmin masuk ke url "/generate-super-admin/"

ikuti flow nya yak, biar gak berantakan

flownya:

## backend
app disesuaikan kalo bisa jangan ngedit app yg bukan tugasnya (pengecualian kalau ada kondisi tertentu diskusi dulu)

{nama app}/models.py -> struktur record per tabel nya, bisa buat method kalau memang dibutuhkan 

{nama app}/views.py -> bussiness layer (logika backend) boleh buat crud 

{nama app}/views/nama_view.py -> buat folder views kalo 1 file views.py terlalu panjang

{nama app}/services/nama_service.py (opsional) -> ini buat logika crud database kalau crudnya kompleks, jika tidak kompleks diperbolehkan pakai views.py saja tidak perlu pakai service

config/urls.py -> route buat penghubung backend dan frontend (intinya buat url, saat url dipanggil frontend eksekusi fungsi di backend)

## frontend

jangan buat desain manual di 1 file html, pakai layout dan pakai component

front end ada di folder templates

templates/layouts -> layout app

templates/components/ui -> component ui contoh: button, input, dll
templates/components/ -> ini buat component yg lebih besar dari ui contoh:sidebar

file html untuk halaman ada di folder 
templates/pages/{nama app}/{nama modul}

kalau mau nambahin js/css tambahan janga lupa pakai {% block extra_js %} atau  {% block extra_css %}

kalau mau nambah icon pakai https://heroicons.com/ copy sebagai svg

## alur ngoding

cek model (tambah method kalau perlu) -> buat fungsi di views.py -> import fungsi dari views.py dipanggil ke urls.py, buat urlnya juga -> buat halaman di templates/pages/{nama app}/{nama modul} -> panggil url di html frontend

udah yak
kalau bingung tanya aja
usahakan ikuti contoh yak
biar gak pusing :v

*btw aku gapake gitignore dulu soalnya gaada credential yang penting







