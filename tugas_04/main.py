"""
Tugas 4 - Enhancement Nomor Ijazah untuk OCR

Alur program:
1. Baca citra ijazah, putar 90 derajat searah jarum jam (file tersimpan miring)
2. Crop area nomor ijazah, ubah ke grayscale
3. Terapkan 3 metode: brightness adjustment, contrast stretching, histogram equalization
4. Jalankan OCR (Tesseract) pada crop asli dan hasil tiap metode
5. Hitung akurasi OCR terhadap ground truth
6. Simpan gambar (citra + histogram sebelum dan sesudah) dan tampilkan ringkasan akurasi

Syarat: Tesseract sudah terpasang dan bisa dipanggil dari terminal (tesseract --version).
"""

import os
from difflib import SequenceMatcher

import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt

# ---------- Lokasi folder (dihitung dari lokasi file ini) ----------
FOLDER_INI = os.path.dirname(os.path.abspath(__file__))
FOLDER_DATA = os.path.join(FOLDER_INI, "..", "data")
FOLDER_OUTPUT = os.path.join(FOLDER_INI, "output")

# ---------- Daftar citra: (nama file, nama kondisi) ----------
DAFTAR_CITRA = [
    ("01_HighQuality_Enhanced.jpg", "Kualitas Tinggi"),
    ("02_LowContrast.jpg", "Kontras Rendah"),
    ("03_Blurred.jpg", "Blur"),
    ("04_HighNoise.jpg", "Noise Tinggi"),
    ("05_LowResolution_Upsampled.jpg", "Resolusi Rendah"),
    ("06_Faded_Underexposed.jpg", "Pudar/Underexposed"),
    ("07_ColorShift_WarmTint.jpg", "Pergeseran Warna"),
    ("08_JPEGCompression_Artifacts.jpg", "Artefak Kompresi JPEG"),
    ("09_CombinedDegradation.jpg", "Degradasi Gabungan"),
]

GROUND_TRUTH = "Nomor ijazah: 571012022000056"
NILAI_BRIGHTNESS = 60

# ---------- Area crop nomor ijazah (persentase, setelah citra diputar) ----------
# Pakai persentase supaya tetap pas walau ukuran citra berbeda
# (citra 08 lebih besar dari citra lainnya).
CROP_ATAS = 0.90
CROP_BAWAH = 0.97
CROP_KIRI = 0.03
CROP_KANAN = 0.31


def baca_citra(nama_file):
    """Baca citra berwarna dari folder data.
    nama_file: nama file citra, contoh "01_HighQuality_Enhanced.jpg"."""
    lokasi = os.path.join(FOLDER_DATA, nama_file)
    citra = cv2.imread(lokasi)
    if citra is None:
        raise FileNotFoundError("Citra tidak ditemukan: " + lokasi)
    return citra


def putar_citra(citra):
    """Putar citra 90 derajat searah jarum jam supaya teks terbaca mendatar.
    cv2.ROTATE_90_CLOCKWISE: arah putaran, searah jarum jam."""
    return cv2.rotate(citra, cv2.ROTATE_90_CLOCKWISE)


def crop_nomor_ijazah(citra):
    """Ambil area nomor ijazah, lalu ubah ke grayscale.
    Crop pakai slicing array: citra[baris_atas:baris_bawah, kolom_kiri:kolom_kanan]."""
    tinggi, lebar = citra.shape[:2]
    atas = int(tinggi * CROP_ATAS)
    bawah = int(tinggi * CROP_BAWAH)
    kiri = int(lebar * CROP_KIRI)
    kanan = int(lebar * CROP_KANAN)
    area = citra[atas:bawah, kiri:kanan]
    return cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)


def brightness_adjustment(gray, nilai=NILAI_BRIGHTNESS):
    """Tambah kecerahan: setiap piksel ditambah 'nilai'.
    cv2.add membatasi hasil maksimal 255 (saturasi). Kalau pakai gray + nilai
    biasa, angka di atas 255 akan 'berputar' balik ke 0 dan merusak citra."""
    return cv2.add(gray, nilai)


def contrast_stretching(gray):
    """Regangkan nilai piksel supaya memenuhi rentang 0 sampai 255.
    cv2.normalize(sumber, tujuan, nilai_min_baru, nilai_maks_baru, jenis):
    - tujuan None   : hasil dibuat sebagai array baru
    - 0 dan 255     : rentang baru yang diinginkan
    - NORM_MINMAX   : nilai terkecil jadi 0, nilai terbesar jadi 255,
                      nilai lain diskalakan secara linear."""
    return cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)


def histogram_equalization(gray):
    """Ratakan sebaran histogram. Hanya menerima citra grayscale 8-bit."""
    return cv2.equalizeHist(gray)


def terapkan_semua_metode(crop):
    """Hasilkan crop asli dan hasil ketiga metode, urutannya tetap."""
    return {
        "Asli (Crop)": crop,
        "Brightness Adjustment": brightness_adjustment(crop),
        "Contrast Stretching": contrast_stretching(crop),
        "Histogram Equalization": histogram_equalization(crop),
    }


def baca_teks_ocr(gray):
    """Jalankan Tesseract pada citra grayscale, hasilnya berupa teks."""
    return pytesseract.image_to_string(gray).strip()


def hitung_akurasi(teks_ocr):
    """Akurasi (persen) = kemiripan teks OCR dengan ground truth.
    SequenceMatcher(None, a, b).ratio() menghasilkan angka 0 sampai 1:
    1 berarti sama persis, 0 berarti sama sekali tidak mirip.
    None artinya tidak ada karakter yang diabaikan."""
    return SequenceMatcher(None, teks_ocr, GROUND_TRUTH).ratio() * 100


def simpan_gambar_perbandingan(nomor, nama_file, kondisi, hasil_metode, akurasi):
    """Simpan satu gambar: baris atas = citra tiap metode (beserta akurasi),
    baris bawah = histogram tiap metode."""
    fig, panel = plt.subplots(2, 4, figsize=(16, 5))

    for kolom, nama_metode in enumerate(hasil_metode):
        gray = hasil_metode[nama_metode]

        panel[0, kolom].imshow(gray, cmap="gray", vmin=0, vmax=255)
        panel[0, kolom].set_title("%s\nacc=%.0f%%" % (nama_metode, akurasi[nama_metode]), fontsize=9)
        panel[0, kolom].axis("off")

        # ravel() meratakan array 2D jadi 1D, bins=256 satu batang per nilai 0-255
        panel[1, kolom].hist(gray.ravel(), bins=256, range=(0, 256), color="black")
        panel[1, kolom].set_title("Histogram - " + nama_metode, fontsize=9)
        panel[1, kolom].set_xlabel("Intensitas piksel")
        panel[1, kolom].set_ylabel("Jumlah piksel")

    fig.suptitle(nama_file.replace(".jpg", "") + " - " + kondisi)
    fig.tight_layout()
    nama_hasil = "hasil_" + str(nomor) + "_" + nama_file.replace(".jpg", "") + ".png"
    fig.savefig(os.path.join(FOLDER_OUTPUT, nama_hasil), dpi=100)
    plt.close(fig)


def simpan_galeri_crop(daftar_crop):
    """Simpan satu gambar berisi crop nomor ijazah dari 9 kondisi (sebelum enhancement).
    daftar_crop: daftar pasangan (nama kondisi, crop grayscale)."""
    fig, panel = plt.subplots(len(daftar_crop), 1, figsize=(8, 11))
    for baris, (kondisi, crop) in enumerate(daftar_crop):
        panel[baris].imshow(crop, cmap="gray", vmin=0, vmax=255)
        panel[baris].set_title(str(baris + 1) + ". " + kondisi, fontsize=8, loc="left")
        panel[baris].axis("off")
    fig.suptitle("Galeri Hasil Crop Area Nomor Ijazah (Sebelum Enhancement) - 9 Kondisi")
    fig.tight_layout()
    fig.savefig(os.path.join(FOLDER_OUTPUT, "galeri_crop.png"), dpi=100)
    plt.close(fig)


def proses_satu_citra(nomor, nama_file, kondisi):
    """Jalankan seluruh tahap untuk satu citra.
    Hasil: crop asli, dan dictionary akurasi tiap metode."""
    citra = putar_citra(baca_citra(nama_file))
    crop = crop_nomor_ijazah(citra)
    hasil_metode = terapkan_semua_metode(crop)

    akurasi = {}
    for nama_metode in hasil_metode:
        teks = baca_teks_ocr(hasil_metode[nama_metode])
        akurasi[nama_metode] = hitung_akurasi(teks)

    simpan_gambar_perbandingan(nomor, nama_file, kondisi, hasil_metode, akurasi)
    return crop, akurasi


def cetak_ringkasan(semua_akurasi):
    """Cetak tabel akurasi tiap kondisi dan rata-ratanya, lalu metode terbaik.
    semua_akurasi: daftar pasangan (nama kondisi, dictionary akurasi)."""
    nama_metode = list(semua_akurasi[0][1].keys())
    print("%-24s" % "Kondisi Citra" + "".join("%-24s" % m for m in nama_metode))

    for kondisi, akurasi in semua_akurasi:
        print("%-24s" % kondisi + "".join("%-24s" % ("%.1f%%" % akurasi[m]) for m in nama_metode))

    rata_rata = {}
    for m in nama_metode:
        rata_rata[m] = float(np.mean([akurasi[m] for kondisi, akurasi in semua_akurasi]))
    print("%-24s" % "Rata-rata" + "".join("%-24s" % ("%.1f%%" % rata_rata[m]) for m in nama_metode))

    # Metode terbaik dipilih hanya dari 3 metode enhancement (tanpa "Asli")
    metode_enhancement = nama_metode[1:]
    terbaik = max(metode_enhancement, key=lambda m: rata_rata[m])
    print("Metode enhancement terbaik (rata-rata akurasi tertinggi):", terbaik)


def main():
    os.makedirs(FOLDER_OUTPUT, exist_ok=True)

    semua_akurasi = []
    daftar_crop = []
    for nomor, (nama_file, kondisi) in enumerate(DAFTAR_CITRA, start=1):
        print("Memproses", nama_file)
        crop, akurasi = proses_satu_citra(nomor, nama_file, kondisi)
        semua_akurasi.append((kondisi, akurasi))
        daftar_crop.append((kondisi, crop))

    simpan_galeri_crop(daftar_crop)
    print()
    cetak_ringkasan(semua_akurasi)
    print("Selesai. Gambar hasil ada di folder:", FOLDER_OUTPUT)


if __name__ == "__main__":
    main()