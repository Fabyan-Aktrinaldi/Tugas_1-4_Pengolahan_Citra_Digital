# Tugas 4: Enhancement Nomor Ijazah untuk OCR

Mata kuliah Pengolahan Citra Digital, Universitas Halu Oleo.
Nama: Fabyan Aktrinaldi | NIM: F1G124029 | Kelas: A

## Catatan penting

Kode ini **disusun ulang** berdasarkan soal dan laporan yang sudah dikumpulkan, karena kode asli hilang. Laporan tidak diubah. Angka akurasi dari kode baru tidak persis sama dengan laporan, perbedaannya dicatat apa adanya di bagian "Perbandingan dengan laporan".

## Soal

Dari citra ijazah, crop area nomor ijazah lalu terapkan brightness adjustment, contrast stretching, dan histogram equalization. Bandingkan ketiganya (citra dan histogram sebelum dan sesudah), tentukan metode terbaik untuk OCR, lalu jawab: mengapa peningkatan kontras membantu OCR, dan apakah histogram equalization selalu metode terbaik.

## Isi folder

- `main.py`: program utama
- `output/`: gambar hasil (dibuat saat program dijalankan, tidak ikut di-push)

## Cara menjalankan

1. Install library dari root repo: `pip install -r requirements.txt`
2. Pasang Tesseract OCR dan pastikan `tesseract --version` bisa dijalankan di terminal (laporan ini diuji dengan Tesseract v5.5.3).
3. Taruh 9 citra dari folder "Praktikum citra" milik dosen di folder `data/` dengan nama aslinya (`01_HighQuality_Enhanced.jpg` sampai `09_CombinedDegradation.jpg`). Citra tidak ikut di-push.
4. Jalankan dari root repo: `python tugas_04/main.py`
5. Hasil: tabel akurasi tercetak di terminal. Di `tugas_04/output/` tersimpan `galeri_crop.png` (crop 9 kondisi) dan `hasil_N_<nama file>.png` (citra dan histogram sebelum dan sesudah enhancement).

## Alur kode

1. `baca_citra` dan `putar_citra`: membaca citra lalu memutar 90 derajat searah jarum jam, karena file tersimpan miring
2. `crop_nomor_ijazah`: mengambil area nomor ijazah lalu mengubahnya ke grayscale
3. `brightness_adjustment`: setiap piksel ditambah 60 dengan `cv2.add` (hasil mentok di 255)
4. `contrast_stretching`: meregangkan nilai piksel ke rentang 0 sampai 255 dengan `cv2.normalize`
5. `histogram_equalization`: meratakan sebaran histogram dengan `cv2.equalizeHist`
6. `baca_teks_ocr` dan `hitung_akurasi`: OCR dengan Tesseract, akurasi dihitung dari kemiripan teks (`SequenceMatcher`) terhadap ground truth `Nomor ijazah: 571012022000056`
7. `simpan_gambar_perbandingan` dan `simpan_galeri_crop`: menyimpan gambar hasil

Area crop ditentukan dengan persentase (baris 90% sampai 97% dari tinggi, kolom 3% sampai 31% dari lebar, setelah citra diputar), bukan koordinat piksel, karena citra `08_JPEGCompression_Artifacts` berukuran lebih besar dari citra lainnya.

## Hasil (kode baru)

Akurasi OCR (%):

| Kondisi Citra | Asli | Brightness Adj. | Contrast Stretch. | Histogram Eq. |
|---|---|---|---|---|
| Kualitas Tinggi | 100.0 | 94.7 | 100.0 | 0.0 |
| Kontras Rendah | 100.0 | 94.7 | 100.0 | 0.0 |
| Blur | 100.0 | 87.7 | 100.0 | 0.0 |
| Noise Tinggi | 100.0 | 94.7 | 100.0 | 0.0 |
| Resolusi Rendah | 100.0 | 94.7 | 100.0 | 0.0 |
| Pudar/Underexposed | 100.0 | 100.0 | 100.0 | 0.0 |
| Pergeseran Warna | 100.0 | 100.0 | 100.0 | 0.0 |
| Artefak Kompresi JPEG | 100.0 | 94.7 | 100.0 | 0.0 |
| Degradasi Gabungan | 100.0 | 100.0 | 100.0 | 0.0 |
| **Rata-rata** | **100.0** | **95.7** | **100.0** | **0.0** |

Metode enhancement dengan rata-rata akurasi tertinggi: **Contrast Stretching**.

## Perbandingan dengan laporan

Akurasi OCR (%), format laporan / kode baru:

| Kondisi Citra | Asli | Brightness Adj. | Contrast Stretch. | Histogram Eq. |
|---|---|---|---|---|
| Kualitas Tinggi | 93.3 / 100.0 | 94.7 / 94.7 | 93.3 / 100.0 | 0.0 / 0.0 |
| Kontras Rendah | 93.3 / 100.0 | 94.7 / 94.7 | 93.3 / 100.0 | 0.0 / 0.0 |
| Blur | 100.0 / 100.0 | 87.7 / 87.7 | 100.0 / 100.0 | 0.0 / 0.0 |
| Noise Tinggi | 96.6 / 100.0 | 94.7 / 94.7 | 96.6 / 100.0 | 0.0 / 0.0 |
| Resolusi Rendah | 100.0 / 100.0 | 94.7 / 94.7 | 100.0 / 100.0 | 0.0 / 0.0 |
| Pudar/Underexposed | 96.7 / 100.0 | 96.7 / 100.0 | 96.7 / 100.0 | 65.5 / 0.0 |
| Pergeseran Warna | 93.3 / 100.0 | 98.2 / 100.0 | 93.3 / 100.0 | 0.0 / 0.0 |
| Artefak Kompresi JPEG | 100.0 / 100.0 | 94.7 / 94.7 | 100.0 / 100.0 | 42.6 / 0.0 |
| Degradasi Gabungan | 100.0 / 100.0 | 100.0 / 100.0 | 100.0 / 100.0 | 0.0 / 0.0 |
| **Rata-rata** | 97.0 / 100.0 | 95.1 / 95.7 | 97.0 / 100.0 | 12.0 / 0.0 |

Angka kode baru tidak persis sama dengan laporan:

- Kolom Brightness Adjustment cocok di 7 dari 9 kondisi. Yang berbeda: Pudar dan Pergeseran Warna.
- Pada kolom Asli dan Contrast Stretching, kode baru membaca 100% di semua kondisi, sedangkan laporan 93.3% sampai 96.7% pada beberapa kondisi.
- Pada Histogram Equalization, kode baru tidak membaca teks sama sekali (0%), sedangkan laporan masih memperoleh 65.5% (Pudar) dan 42.6% (Artefak JPEG).

Dugaan penyebab: koordinat crop asli hilang sehingga area crop ditentukan ulang dari gambar galeri di laporan, dan hasil OCR sangat sensitif terhadap area crop (tepi, titik-titik kecil di dekat nomor) serta versi Tesseract. Kesimpulan akhirnya tetap sama dengan laporan: Contrast Stretching setara atau lebih baik dari citra asli dan paling aman, Brightness Adjustment sedikit menurunkan akurasi, Histogram Equalization paling buruk.

## Metode terbaik untuk OCR

Contrast Stretching. Akurasinya sama dengan citra asli di semua kondisi pada percobaan ini, jadi ia tidak merusak bentuk karakter, dan pada citra pudar ia mengembalikan latar yang terang. Perlu dicatat, pada citra yang sudah terbaca 100% (hampir semua kondisi), Contrast Stretching tidak menambah akurasi, hanya tidak menguranginya. Brightness Adjustment kadang menurunkan akurasi (misalnya Blur) karena penambahan nilai tetap membuat area terang jenuh di 255. Histogram Equalization paling tidak stabil.

## Mengapa peningkatan kontras membantu OCR?

OCR memisahkan piksel karakter dari latar (binarisasi) sebelum mengenali bentuknya. Kontras rendah membuat batas karakter dan latar kabur sehingga pemisahan mudah salah. Meningkatkan kontras memperlebar jarak intensitas antara karakter dan latar, sehingga tepi karakter lebih tegas dan bentuknya lebih mudah dikenali.

## Apakah histogram equalization selalu metode terbaik?

Tidak. Pada percobaan ini Histogram Equalization justru terburuk: akurasi 0% di semua kondisi pada kode baru, dan di laporan hanya membantu pada kondisi Pudar/Underexposed (65.5%) dan sedikit pada Artefak JPEG (42.6%), yaitu saat histogram aslinya sangat sempit. Pada kondisi lain metode ini terlalu agresif: ikut meregangkan noise dan tekstur kertas sehingga latar menjadi berbintik dan menutupi karakter. Jadi histogram equalization hanya cocok untuk citra berkontras sangat rendah, bukan solusi umum.