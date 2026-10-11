# Tugas 3: Analisis Citra Ijazah

Mata kuliah Pengolahan Citra Digital, Universitas Halu Oleo.
Nama: Fabyan Aktrinaldi | NIM: F1G124029 | Kelas: A

## Catatan penting

Kode ini **disusun ulang** berdasarkan soal dan laporan yang sudah dikumpulkan, karena kode asli hilang. Laporan tidak diubah. Angka dari kode baru dibandingkan dengan laporan di bagian "Perbandingan dengan laporan".

## Soal

Diberikan 9 citra ijazah dengan kondisi pencahayaan dan kualitas berbeda. Setiap citra diubah ke grayscale, ditampilkan histogram citra asli dan grayscale, dianalisis distribusi intensitas pikselnya, lalu diidentifikasi masalahnya (terlalu gelap, terlalu terang, kontras rendah, pencahayaan tidak merata, atau noise) dan ditentukan metode enhancement yang sesuai.

## Isi folder

- `main.py`: program utama
- `output/`: gambar hasil (dibuat saat program dijalankan, tidak ikut di-push)

## Cara menjalankan

1. Install library dari root repo: `pip install -r requirements.txt`
2. Taruh 9 citra dari folder "Praktikum citra" milik dosen di folder `data/` dengan nama aslinya (`01_HighQuality_Enhanced.jpg` sampai `09_CombinedDegradation.jpg`). Citra tidak ikut di-push.
3. Jalankan dari root repo: `python tugas_03/main.py`
4. Hasil: ringkasan tercetak di terminal, dan gambar `hasil_N_<nama file>.png` tersimpan di `tugas_03/output/`. Tiap gambar berisi citra asli, grayscale, histogram RGB, dan histogram grayscale.


## Citra yang dipakai

Nomor citra mengikuti laporan Tugas 3. Di laporan, citra dinamai `ijazah1.jpg` sampai `ijazah9.jpg` dengan urutan yang berbeda dari urutan folder dosen. Di repo ini dipakai nama asli dari dosen, dengan pemetaan berikut:

| Citra di laporan | File di folder `data/` |
|---|---|
| 1 | `06_Faded_Underexposed.jpg` |
| 2 | `04_HighNoise.jpg` |
| 3 | `07_ColorShift_WarmTint.jpg` |
| 4 | `01_HighQuality_Enhanced.jpg` |
| 5 | `03_Blurred.jpg` |
| 6 | `05_LowResolution_Upsampled.jpg` |
| 7 | `02_LowContrast.jpg` |
| 8 | `08_JPEGCompression_Artifacts.jpg` |
| 9 | `09_CombinedDegradation.jpg` 


## Alur kode

1. `baca_citra`: membaca citra berwarna (urutan BGR)
2. `ubah_ke_grayscale`: konversi ke abu-abu dengan `cv2.cvtColor`
3. `hitung_statistik`: menghitung mean dan std intensitas piksel
4. `cek_tidak_merata` dan `diagnosis_citra`: menentukan masalah citra
5. `pilih_enhancement`: memilih metode enhancement sesuai masalah
6. `simpan_gambar_analisis`: membuat dan menyimpan gambar 4 panel

## Aturan diagnosis

| Kondisi | Masalah |
|---|---|
| mean < 85 | Terlalu gelap |
| mean > 170 | Terlalu terang |
| std < 40 | Kontras rendah |
| std > 75 | Kemungkinan noise tinggi |
| selisih mean antar sisi citra > 40 | Pencahayaan tidak merata |

Batas mean dan std mengikuti laporan. Batas selisih antar sisi (40) tidak tertulis di laporan, jadi dipilih saat menyusun ulang kode.

## Hasil (sesuai laporan)

| No | Mean | Std | Masalah | Metode Enhancement |
|---|---|---|---|---|
| 1 | 154.9 | 15.8 | Kontras rendah | Histogram Equalization |
| 2 | 231.4 | 34.3 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 3 | 231.3 | 33.3 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 4 | 237.8 | 39.3 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 5 | 239.7 | 28.3 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 6 | 239.5 | 32.1 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 7 | 239.5 | 20.8 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 8 | 239.2 | 34.2 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |
| 9 | 184.6 | 21.8 | Terlalu terang, kontras rendah | Gamma Correction, Histogram Equalization |

## Perbandingan dengan laporan

Kode ini sudah dijalankan pada kesembilan citra. Hasilnya:

- Nilai mean dan std untuk Citra 1 sampai 9 sama dengan laporan.
- Diagnosis masalah dan metode enhancement yang dihasilkan juga sama dengan laporan.
- Tidak ada citra yang terdeteksi memiliki pencahayaan tidak merata atau noise tinggi, sesuai laporan.

Dua perbedaan kecil yang tidak memengaruhi isi laporan: (1) di laporan citra dinamai `ijazah1.jpg` sampai `ijazah9.jpg`, sedangkan di repo ini dipakai nama asli dari dosen (lihat tabel pemetaan di atas); (2) nama file gambar hasil kini `hasil_N_<nama file>.png`, sedangkan di laporan dulu `hasil_N_ijazahN.jpg.png`. Tampilan gambar (citra asli, grayscale, histogram RGB, histogram grayscale) mengikuti laporan.

## Apakah histogram yang lebih tersebar selalu lebih baik?

Tidak selalu. Std hanya menunjukkan lebar sebaran nilai piksel, bukan posisinya di rentang 0 sampai 255 dan bukan apakah ada clipping (piksel menumpuk di ujung skala). Contohnya Citra 4 punya std tertinggi di kelompok citra terang (39,3) tetapi tetap overexposed karena histogramnya menumpuk dekat 255. Kualitas citra lebih ditentukan oleh seberapa penuh rentang 0 sampai 255 dimanfaatkan tanpa clipping, bukan hanya oleh lebar sebaran.