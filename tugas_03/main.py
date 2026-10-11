"""
Tugas 3 - Analisis Citra Ijazah

Alur program:
1. Baca citra ijazah (BGR) dari folder data
2. Ubah ke grayscale
3. Hitung mean dan std intensitas piksel grayscale
4. Diagnosis masalah citra (gelap, terang, kontras rendah, tidak merata, noise)
5. Pilih metode enhancement sesuai masalah
6. Simpan gambar: citra asli, grayscale, histogram RGB, histogram grayscale
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# ---------- Lokasi folder (dihitung dari lokasi file ini) ----------
FOLDER_INI = os.path.dirname(os.path.abspath(__file__))
FOLDER_DATA = os.path.join(FOLDER_INI, "..", "data")
FOLDER_OUTPUT = os.path.join(FOLDER_INI, "output")

# ---------- Daftar citra, urutannya mengikuti Citra 1 sampai 9 di laporan ----------
# Nama file adalah nama asli dari folder "Praktikum citra" milik dosen.
DAFTAR_CITRA = [
    "06_Faded_Underexposed.jpg",         # Citra 1 di laporan
    "04_HighNoise.jpg",                  # Citra 2
    "07_ColorShift_WarmTint.jpg",        # Citra 3
    "01_HighQuality_Enhanced.jpg",       # Citra 4
    "03_Blurred.jpg",                    # Citra 5
    "05_LowResolution_Upsampled.jpg",    # Citra 6
    "02_LowContrast.jpg",                # Citra 7
    "08_JPEGCompression_Artifacts.jpg",  # Citra 8
    "09_CombinedDegradation.jpg",        # Citra 9
]

# ---------- Batas diagnosis (sesuai laporan) ----------
BATAS_GELAP = 85            # mean di bawah ini = terlalu gelap
BATAS_TERANG = 170          # mean di atas ini = terlalu terang
BATAS_KONTRAS_RENDAH = 40   # std di bawah ini = kontras rendah
BATAS_NOISE = 75            # std di atas ini = kemungkinan noise tinggi
BATAS_TIDAK_MERATA = 40     # selisih mean antar sisi citra


def baca_citra(nama_file):
    """Baca citra berwarna dari folder data.
    nama_file: nama file citra, contoh "ijazah1.jpg"
    Hasil: array BGR (OpenCV membaca urutan warna Biru-Hijau-Merah)."""
    lokasi = os.path.join(FOLDER_DATA, nama_file)
    citra = cv2.imread(lokasi)
    if citra is None:
        raise FileNotFoundError("Citra tidak ditemukan: " + lokasi)
    return citra


def ubah_ke_grayscale(citra_bgr):
    """Ubah citra berwarna jadi grayscale.
    citra_bgr: citra hasil cv2.imread
    cv2.COLOR_BGR2GRAY: jenis konversinya, dari BGR ke abu-abu."""
    return cv2.cvtColor(citra_bgr, cv2.COLOR_BGR2GRAY)


def hitung_statistik(gray):
    """Hitung rata-rata (mean) dan simpangan baku (std) intensitas piksel.
    mean tinggi = citra terang, std kecil = sebaran sempit (kontras rendah)."""
    mean = float(np.mean(gray))
    std = float(np.std(gray))
    return mean, std


def cek_tidak_merata(gray):
    """Cek pencahayaan tidak merata.
    Citra dibagi dua (kiri-kanan dan atas-bawah), lalu mean tiap sisi dibandingkan.
    Hasil True kalau ada sisi yang jauh lebih gelap/terang dari sisi lainnya."""
    tinggi, lebar = gray.shape
    kiri = np.mean(gray[:, : lebar // 2])
    kanan = np.mean(gray[:, lebar // 2:])
    atas = np.mean(gray[: tinggi // 2, :])
    bawah = np.mean(gray[tinggi // 2:, :])
    selisih = max(abs(kiri - kanan), abs(atas - bawah))
    return selisih > BATAS_TIDAK_MERATA


def diagnosis_citra(mean, std, tidak_merata):
    """Tentukan daftar masalah citra dari mean, std, dan hasil cek merata."""
    masalah = []
    if mean < BATAS_GELAP:
        masalah.append("Terlalu gelap (mean rendah)")
    if mean > BATAS_TERANG:
        masalah.append("Terlalu terang (mean tinggi)")
    if std < BATAS_KONTRAS_RENDAH:
        masalah.append("Kontras rendah (histogram sempit/mengumpul)")
    if std > BATAS_NOISE:
        masalah.append("Kemungkinan noise tinggi (std tinggi)")
    if tidak_merata:
        masalah.append("Pencahayaan tidak merata")
    return masalah


def pilih_enhancement(masalah):
    """Pilih metode enhancement untuk tiap masalah.
    Hasil: daftar (nama metode, alasan)."""
    saran = {
        "Terlalu gelap": ("Gamma Correction (gamma < 1)",
                          "menaikkan intensitas piksel yang terlalu gelap agar detail terlihat."),
        "Terlalu terang": ("Gamma Correction (gamma > 1)",
                           "menurunkan intensitas piksel yang overexposed agar detail tidak hilang."),
        "Kontras rendah": ("Histogram Equalization",
                           "melebarkan rentang intensitas piksel supaya detail lebih terlihat jelas."),
        "Kemungkinan noise": ("Median/Gaussian Filter",
                              "meratakan noise tanpa menghilangkan terlalu banyak detail."),
        "Pencahayaan tidak merata": ("CLAHE (Adaptive Histogram Equalization)",
                                     "memperbaiki kontras per bagian citra, bukan satu nilai untuk seluruh citra."),
    }
    hasil = []
    for teks in masalah:
        for kunci in saran:
            if teks.startswith(kunci):
                hasil.append(saran[kunci])
    return hasil


def simpan_gambar_analisis(nomor, nama_file, citra_bgr, gray, mean, std):
    """Buat satu gambar berisi 4 panel lalu simpan ke folder output:
    kiri atas = citra asli, kanan atas = grayscale,
    kiri bawah = histogram RGB, kanan bawah = histogram grayscale."""
    fig, panel = plt.subplots(2, 2, figsize=(10, 8))

    # Panel 1: citra asli. imshow butuh urutan RGB, jadi BGR diubah dulu.
    panel[0, 0].imshow(cv2.cvtColor(citra_bgr, cv2.COLOR_BGR2RGB))
    panel[0, 0].set_title("Citra Asli - " + nama_file)
    panel[0, 0].axis("off")

    # Panel 2: grayscale. vmin=0 dan vmax=255 supaya skala abu-abu tidak
    # ditarik otomatis oleh matplotlib (kalau ditarik, kontras jadi menipu).
    panel[0, 1].imshow(gray, cmap="gray", vmin=0, vmax=255)
    panel[0, 1].set_title("Citra Grayscale")
    panel[0, 1].axis("off")

    # Panel 3: histogram tiap kanal warna.
    # cv2.calcHist(gambar, kanal, mask, jumlah_bin, rentang_nilai)
    for nomor_kanal, warna in enumerate(["b", "g", "r"]):
        hist = cv2.calcHist([citra_bgr], [nomor_kanal], None, [256], [0, 256])
        panel[1, 0].plot(hist, color=warna)
    panel[1, 0].set_title("Histogram Citra Asli (RGB)")
    panel[1, 0].set_xlabel("Intensitas piksel")
    panel[1, 0].set_ylabel("Jumlah piksel")

    # Panel 4: histogram grayscale.
    # ravel() meratakan array 2D jadi 1D, bins=256 satu batang per nilai 0-255.
    panel[1, 1].hist(gray.ravel(), bins=256, range=(0, 256), color="black")
    panel[1, 1].set_title("Histogram Grayscale (mean=%.1f, std=%.1f)" % (mean, std))
    panel[1, 1].set_xlabel("Intensitas piksel")
    panel[1, 1].set_ylabel("Jumlah piksel")

    fig.tight_layout()
    nama_hasil = "hasil_" + str(nomor) + "_" + nama_file.replace(".jpg", "") + ".png"
    fig.savefig(os.path.join(FOLDER_OUTPUT, nama_hasil), dpi=100)
    plt.close(fig)  # tutup supaya memori tidak menumpuk


def proses_satu_citra(nomor, nama_file):
    """Jalankan seluruh tahap untuk satu citra, lalu kembalikan ringkasannya."""
    citra_bgr = baca_citra(nama_file)
    gray = ubah_ke_grayscale(citra_bgr)
    mean, std = hitung_statistik(gray)
    masalah = diagnosis_citra(mean, std, cek_tidak_merata(gray))
    saran = pilih_enhancement(masalah)
    simpan_gambar_analisis(nomor, nama_file, citra_bgr, gray, mean, std)
    return mean, std, masalah, saran


def main():
    os.makedirs(FOLDER_OUTPUT, exist_ok=True)

    print("No | Mean  | Std  | Masalah | Metode Enhancement")
    for nomor, nama_file in enumerate(DAFTAR_CITRA, start=1):
        mean, std, masalah, saran = proses_satu_citra(nomor, nama_file)
        print("%d | %.1f | %.1f | %s | %s" % (
            nomor, mean, std,
            "; ".join(masalah),
            ", ".join(nama for nama, alasan in saran)))

    print("Selesai. Gambar hasil ada di folder:", FOLDER_OUTPUT)


if __name__ == "__main__":
    main()