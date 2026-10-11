# Praktikum Pengolahan Citra Digital (Tugas 1 sampai 4)

Nama: Fabyan Aktrinaldi | NIM: F1G124029 | Kelas: A
Mata kuliah: Pengolahan Citra Digital, Universitas Halu Oleo
Dosen: Muhammad Riansyah Tohamba, S.T., M.Kom.

## Isi repo

Repo ini berisi Tugas 1 sampai 4. Tugas 5, 6, dan 7 ada di repo terpisah (lihat tabel).

| Tugas | Topik | Isi | Status kode | Link |
|---|---|---|---|---|
| 1 | Review Matrix Multiplication (perkalian matriks array 3 dimensi, CLI Python) | Kode dan gambar output | Kode asli | [tugas_01](https://github.com/Fabyan-Aktrinaldi/Tugas_1-4_Pengolahan_Citra_Digital/tree/main/tugas_01) |
| 2 | Warna pada Citra Digital (kanal BGR dan alternatifnya) | Laporan teori (PDF), tidak ada kode | Tidak ada kode | [tugas_02](https://github.com/Fabyan-Aktrinaldi/Tugas_1-4_Pengolahan_Citra_Digital/tree/main/tugas_02) |
| 3 | Analisis Citra Ijazah (grayscale, histogram, diagnosis, enhancement) | Kode dan README | Disusun ulang | [tugas_03](https://github.com/Fabyan-Aktrinaldi/Tugas_1-4_Pengolahan_Citra_Digital/tree/main/tugas_03) |
| 4 | Enhancement Nomor Ijazah untuk OCR | Kode dan README | Disusun ulang | [tugas_04](https://github.com/Fabyan-Aktrinaldi/Tugas_1-4_Pengolahan_Citra_Digital/tree/main/tugas_04) |
| 5 | Enhancement untuk OCR (filter mean, median, Gaussian, dan sharpening) | Repo terpisah | [ISI: kode asli] | [ISI LINK REPO TUGAS 5] |
| 6 | Deteksi tanda tangan | Repo terpisah | [ISI] | [ISI LINK REPO TUGAS 6] |
| 7 | Mini project integrasi | Repo terpisah | [ISI] | [ISI LINK REPO TUGAS 7] |

## Catatan tentang kode

- **Tugas 1**: kode dan output adalah file yang dikumpulkan saat tugas itu dikerjakan.
- **Tugas 2**: soal teori, jadi tidak ada kode. Jawaban ada di file PDF di folder `tugas_02`.
- **Tugas 3 dan 4**: kode asli hilang, sehingga **disusun ulang** berdasarkan soal dan laporan yang sudah dikumpulkan (laporan tidak diubah). Angka dari kode baru dibandingkan dengan laporan, dan perbedaannya dicatat apa adanya di README masing-masing tugas.

## Struktur folder

```
Tugas_1-4_Pengolahan_Citra_Digital/
├── README.md
├── requirements.txt
├── .gitignore
├── data/            (citra ijazah, tidak di-push)
├── tugas_01/        (kode asli dan gambar output)
├── tugas_02/        (laporan teori, PDF)
├── tugas_03/        (main.py, README.md)
└── tugas_04/        (main.py, README.md)
```

Folder `data/` dan isi `output/` di tiap tugas tidak ikut di-push (diatur di `.gitignore`). Gambar hasil dibuat otomatis saat program dijalankan.

## Cara menjalankan

1. Clone repo ini, lalu install library: `pip install -r requirements.txt`
2. Untuk Tugas 3 dan 4, taruh 9 citra ijazah dari folder "Praktikum citra" milik dosen di folder `data/` dengan nama aslinya (`01_HighQuality_Enhanced.jpg` sampai `09_CombinedDegradation.jpg`).
3. Khusus Tugas 4, pasang juga Tesseract OCR dan pastikan `tesseract --version` bisa dijalankan di terminal.
4. Jalankan dari root repo, contoh:
   - `python tugas_03/main.py`
   - `python tugas_04/main.py`

Petunjuk lebih rinci ada di README tiap folder tugas.