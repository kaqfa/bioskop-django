# Recap Hari 1

Sebaiknya menggunakan Python3 dan tambahan tool seperti pip, 
(virtualenv, virtualenvwrapper), bisa install Anaconda yang sudah tersedia 
virtual environment (conda env).

Instalasi django dengan command prompt (harus terkoneksi internet)

```
pip install django
```

### Memulai project
```
django-admin startproject tutorial_bioskop
cd nama-project
python manage.py startapp movie
```

### Create User & setup database
```python
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- web bisa diakses di localhost:8000
- halaman admin bisa diakses di localhost:8000/admin
- untuk mengganti url admin bisa edit ```tutorial_bioskop/urls.py```

### Include app ke project
- ```tutorial_bioskop/settings.py``` edit bagian :
```python
INSTALLED_APPS = [
    ...
    'movie',
]
```

### Selanjutnya
- Membuat model movie ```movie/models.py```
- Membuat admin untuk movie ```movie/admin.py```
- buat skrip migrasi  ```python manage.py makemigrations```
- menerapkan migrasi ke database ```python manage.py migrate```


# Recap Hari 2

Possible modification untuk admin itu:

- **list_display** : menentukan field apa saja yang ditampilkan pada tabel, termasuk
    kita bisa menampilkan method dari model yang return string.
- **fields** : untuk menentukan field apa saja yang tampil pada form
- untuk melakukan override pada prosedur simpan, bisa menggunakan **save_model**

Memberikan tambahan fungsi pada model, untuk memudahkan modifikasi dan memproses
data pada model tersebut. Contoh:

- **show_genres** : untuk mengembalikan semua genre yang dimiliki dalam bentuk string
- **in_show** : untuk mengmbalikan status tayang movie dengan integer
- **show_status** : untuk mengembalikan status tayang movie dengan string

### Menggunakan View & Template untuk Tampilan (bukan admin)

Prosedurnya menampilkan tampilan:

- modifikasi setting untuk menetukan direktori Template (one time)
```python
TEMPLATES = [
    {   ...
        'DIRS': ['templates'],
    ... } ]
```
- Membuat halaman HTML untuk halaman depan
- Membuat Class Generic View (extends dari ListView) untuk index.html
- Membuat URL untuk mengakses view yang sudah dibuat.


# Recap Hari 3

### Menambahkan staticfile (CSS, JS, Image)

- menambahkan static dirs pada settings.py
```python
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
```
- di bagian paling atas ditambahkan ```{% load static %}```
- bagian yang memanggil static files diberikan keyword ```static``` contohnya
```html
<link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
<script src="{% static 'js/bootstrap.min.js' %}"></script>
```
- jangan lupa file static sudah dimasukkan ke direktori static yang sudah 
  dideklarasikan pada settings.py

### Melakukan extends templates

- template yang digunakan bisa extends dari template lain caranya dengan menambahkan
  perintah ```{% extends template_yang_ingin_diextend.html %}``` pada baris paling atas.
  bahkan di atas ```{% load static %}```.
- pada super template-nya diberikan ```{% block namablock %} {% endblock %}``` untuk
  tempat menyisipkan konten tambahan pada sub template.
- kemudian pada sub template tinggal mengisikan 
  ```{% block namablock %} konten baru {% endblock %}``` untuk menambahkan konten.

### Tambahan

- template bersifat dumb, artinya tidak semua perintah python dapat diekseskusi di template
- untuk mengeksekusi perintah menggunakan tag ```{%  %}```
- untuk menampilkan nilai (variabel) menggunakan tag ```{{  }}```


# Recap Hari 4

### Membuat Halaman Login & Logout

Login & Logout lebih mudah menggunakan fungsi view yang telah disedikan django.
Langkahnya adalah:

- tambahkan ```views.login``` dan ```views.logout``` pada ```urls.py```
```python
urlpatterns = [
    url(r'^login/', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', views.logout, {'next_page': 'index'}, name='logout'),
    # ...
]
```
- buat template html untuk halaman login
- set ```LOGIN_REDIRECT_URL``` pada halaman ```settings.py```
- (*additional*) Tambahkan link ke halaman login pada index (sidebar)
- **DONE**

### Membuat halaman registrasi

- Generate aplikasi baru dengan menjalankan perintah di terminal
```
python manage.py startapp member
```
- Tambahkan model untuk member yang berrelasi *one-to-one* dengan tabel ```django.contrib.auth.models.User```
- Buat file ```forms.py``` pada aplikasi member.
- Tambahkan 2 form yaitu ```UserForm``` dan ```MemberForm```
- Tambahkan attribute ```password```, ```pass_confirm```, dan ```email``` untuk disesuaikan.
- Override method ```clean_username(self)``` untuk mengecek username yang diinputkan belum pernah digunakan
- Override method ```clean(self)``` untuk memastikan password dan konfirmasinya sudah sama
- untuk ```MemberForm``` tambah saja field yang ingi dipakai
- buat template untuk register dan tambahkan form
- buat FBV untuk register sebagai berikut:
```python
def register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        memberform = MemberForm(request.POST)
        if userform.is_valid() * memberform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()
            member = memberform.save(commit=False)
            member.user = user
            member.save()
            return redirect('index')
    else:
        userform = UserForm()
        memberform = MemberForm()
    return render(request, 'register.html', {'userform':userform, 'memberform':memberform})
```
- jangan lupa buat juga URL-nya
- (*optional*) buat link register di halaman index



# Recap Hari 5

### Model dan Admin untuk TopUp

- Buat model untuk TopUp di aplikasi ```Member```
- Buat admin untuk ```MemberAdmin``` dan ```TopUpAdmin```
- Pada halaman admin untuk member tambahkan saja ```list_display``` yang 
  akan digunakan
- Pada halaman admin untuk TopUp tambahkan ```list_display``` dan juga
  ```fields``` yang diperlukan saja.
- Override ```save_models(self, request, obj, form, change)``` untuk
  memastikan kolom ```checked_by``` akan otomatis berisi ```reques.user```
  
### Halaman Form untuk TopUp

- Tambahkan ```TopUpForm``` dengan memilih field yang diperlukan saja
- Buat juga template html untuk form topup
- Untuk menghubungkan antara template dengan form dan model, buat view
  yang extends dari ```CreateView```
- Override ```form_valid(self, form)``` untuk memastikan field member
  berisi member yang aktif saat ini dan status menjadi **pending**
- Terakhir tambahkan URL untuk View form yang telah dibuat

### List TopUp milik Member

- Buat ```TopUpListView``` yang extend dari ```ListView```
- Override ```get_queryset(self)``` untuk memastikan hanya TopUp milik 
  member yang saat ini sedang login saja yang ditampilkan
- Buat template HTML untuk menampilkan View tersebut dalam bentuk tabel
- Terakhir tambahkan URL untuk View yang telah dibuat

### Admin Action untuk Validate & Invalidate

- Pada ```TopUpAdmin``` tambahkan method ```check_validate``` dan ```check_invalidate```

```python
    def accept_topup(self, request, queryset):
        queryset.update(status='a')
    accept_topup.short_description = "Validasi Topup"

    def deny_topup(self, request, queryset):
        queryset.update(status='d')
    deny_topup.short_description = 'Invalidasi Topup'
```

- Tambahkan kedua method tersebut pada attribute ```actions```



# Recap Hari 6

*NB: Jika kesulitan menggunakan CBV, back to FBV is okay* 

- 
