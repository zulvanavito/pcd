# Impor modul yang diperlukan
from PIL import Image, ImageOps  # Modul PIL untuk memproses dan memanipulasi gambar
import math  # Modul matematika untuk fungsi logaritma pada transformasi logaritmik

# Fungsi untuk mengubah gambar menjadi negatif
def ImgNegative(img_input, coldepth):
    """
    Mengubah gambar menjadi negatif berdasarkan kedalaman warna dengan membalik nilai RGB.
    
    Args:
        img_input (PIL.Image): Objek gambar input yang akan diproses menjadi negatif.
        coldepth (int): Kedalaman warna gambar (1 untuk biner, 8 untuk grayscale, 24/32 untuk RGB/RGBA).
    
    Returns:
        PIL.Image: Objek gambar output dalam bentuk negatif.
    """
    # Konversi gambar ke mode RGB jika bukan 24-bit untuk memudahkan manipulasi warna
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat gambar baru dengan mode RGB dan ukuran yang sama dengan input
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()  # Akses piksel gambar output untuk manipulasi langsung
    
    # Iterasi setiap piksel untuk membalik nilai RGB (negatif = 255 - nilai asli)
    for i in range(img_output.size[0]):  # Loop melalui lebar gambar
        for j in range(img_output.size[1]):  # Loop melalui tinggi gambar
            r, g, b = img_input.getpixel((i, j))  # Ambil nilai RGB dari piksel input
            pixels[i, j] = (255 - r, 255 - g, 255 - b)  # Simpan nilai negatif ke piksel output
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna yang diberikan
    if coldepth == 1:
        img_output = img_output.convert("1")  # Konversi ke mode biner (1-bit, hitam-putih)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Konversi ke mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Tetap di mode RGB (24-bit atau lebih)
    
    return img_output  # Kembalikan gambar hasil negatif

def ImgRotate(img_input, coldepth, deg):
    """
    Memutar gambar berdasarkan sudut tertentu (dalam derajat).
    Sudut positif untuk clockwise, sudut negatif untuk counterclockwise.
    
    Args:
        img_input (PIL.Image): Objek gambar input yang akan diputar.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        deg (float): Derajat rotasi (positif untuk clockwise, negatif untuk counterclockwise).
    
    Returns:
        PIL.Image: Objek gambar output yang telah diputar.
    """
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Dalam PIL, rotate(deg) memutar counterclockwise untuk sudut positif
    # Untuk clockwise, kita perlu sudut negatif
    rotation_angle = -deg  # Balik sudut untuk membuat positif = clockwise
    img_output = img_input.rotate(rotation_angle, expand=True, fillcolor=(0, 0, 0))
    
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

# Fungsi untuk menyesuaikan kecerahan gambar
def ImgBrightness(img_input, coldepth, factor):
    """
    Menyesuaikan kecerahan gambar dengan menambah atau mengurangi nilai piksel RGB.
    
    Args:
        img_input (PIL.Image): Objek gambar input yang akan disesuaikan kecerahannya.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        factor (float): Nilai penyesuaian kecerahan (-255 hingga 255); positif untuk lebih terang, negatif untuk lebih gelap.
    
    Returns:
        PIL.Image: Objek gambar dengan kecerahan yang telah disesuaikan.
    """
    # Konversi gambar ke mode RGB jika bukan 24-bit untuk memudahkan manipulasi warna
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat gambar baru dengan ukuran yang sama untuk menyimpan hasil penyesuaian
    img_output = Image.new('RGB', img_input.size)
    pixels = img_output.load()  # Akses piksel gambar output untuk manipulasi
    
    # Iterasi setiap piksel untuk menyesuaikan kecerahan
    for i in range(img_output.size[0]):  # Loop melalui lebar gambar
        for j in range(img_output.size[1]):  # Loop melalui tinggi gambar
            r, g, b = img_input.getpixel((i, j))  # Ambil nilai RGB dari piksel input
            # Tambah atau kurangi nilai RGB dengan faktor, batasi antara 0 dan 255
            r = max(0, min(255, r + int(factor)))
            g = max(0, min(255, g + int(factor)))
            b = max(0, min(255, b + int(factor)))
            pixels[i, j] = (r, g, b)  # Simpan nilai baru ke piksel output
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna
    if coldepth == 1:
        img_output = img_output.convert("1")  # Konversi ke mode biner (1-bit)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Konversi ke mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Tetap di mode RGB (24-bit atau lebih)
    
    return img_output  # Kembalikan gambar dengan kecerahan baru

# Fungsi untuk mencampur dua gambar (blending)
def ImgBlending(img_input1, img_input2, coldepth, alpha):
    """
    Menggabungkan dua gambar menggunakan faktor alpha (linear blending).
    
    Args:
        img_input1 (PIL.Image): Objek gambar pertama sebagai dasar pencampuran.
        img_input2 (PIL.Image): Objek gambar kedua yang akan dicampur.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        alpha (float): Faktor blending (0.0 hingga 1.0); 1.0 = 100% img_input1, 0.0 = 100% img_input2.
    
    Returns:
        PIL.Image: Objek gambar hasil pencampuran dua gambar.
    """
    # Pastikan gambar pertama dalam mode RGB jika bukan 24-bit
    if coldepth != 24:
        img_input1 = img_input1.convert('RGB')
    # Konversi gambar kedua ke RGB dan sesuaikan ukurannya dengan gambar pertama
    img_input2 = img_input2.convert('RGB').resize(img_input1.size)
    
    # Buat gambar baru untuk menyimpan hasil blending dengan ukuran sama seperti gambar pertama
    img_output = Image.new('RGB', img_input1.size)
    pixels = img_output.load()  # Akses piksel gambar output untuk manipulasi
    
    # Batasi nilai alpha agar selalu antara 0.0 dan 1.0
    alpha = max(0.0, min(1.0, alpha))
    
    # Iterasi setiap piksel untuk menghitung nilai campuran berdasarkan alpha
    for i in range(img_output.size[0]):  # Loop melalui lebar gambar
        for j in range(img_output.size[1]):  # Loop melalui tinggi gambar
            r1, g1, b1 = img_input1.getpixel((i, j))  # Ambil nilai RGB dari gambar pertama
            r2, g2, b2 = img_input2.getpixel((i, j))  # Ambil nilai RGB dari gambar kedua
            # Hitung nilai campuran dengan rumus: (alpha * img1) + ((1 - alpha) * img2)
            r = int(r1 * alpha + r2 * (1 - alpha))
            g = int(g1 * alpha + g2 * (1 - alpha))
            b = int(b1 * alpha + b2 * (1 - alpha))
            # Pastikan nilai RGB tetap dalam rentang 0-255
            pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna
    if coldepth == 1:
        img_output = img_output.convert("1")  # Konversi ke mode biner (1-bit)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Konversi ke mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Tetap di mode RGB (24-bit atau lebih)
    
    return img_output  # Kembalikan gambar hasil blending

# Fungsi untuk transformasi logaritmik pada gambar
def ImgLogarithmic(img_input, coldepth, c):
    """
    Menerapkan transformasi logaritmik untuk meningkatkan detail di area gelap gambar.
    
    Args:
        img_input (PIL.Image): Objek gambar input yang akan diproses.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        c (float): Konstanta skala untuk mengatur intensitas transformasi logaritmik.
    
    Returns:
        PIL.Image: Objek gambar dengan transformasi logaritmik.
    """
    # Konversi gambar ke mode RGB jika bukan 24-bit untuk memudahkan manipulasi warna
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat gambar baru dengan ukuran yang sama untuk menyimpan hasil transformasi
    img_output = Image.new('RGB', img_input.size)
    pixels = img_output.load()  # Akses piksel gambar output untuk manipulasi
    
    # Iterasi setiap piksel untuk menerapkan transformasi logaritmik
    for i in range(img_output.size[0]):  # Loop melalui lebar gambar
        for j in range(img_output.size[1]):  # Loop melalui tinggi gambar
            r, g, b = img_input.getpixel((i, j))  # Ambil nilai RGB dari piksel input
            # Terapkan rumus logaritmik: c * log(1 + nilai) untuk setiap kanal warna
            r = int(c * math.log(1 + r))  # Tambah 1 untuk menghindari log(0)
            g = int(c * math.log(1 + g))
            b = int(c * math.log(1 + b))
            # Pastikan nilai RGB tetap dalam rentang 0-255
            pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna
    if coldepth == 1:
        img_output = img_output.convert("1")  # Konversi ke mode biner (1-bit)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Konversi ke mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Tetap di mode RGB (24-bit atau lebih)
    
    return img_output  # Kembalikan gambar hasil transformasi logaritmik

# Fungsi untuk transformasi power-law (gamma correction)
def ImgPowerLaw(img_input, coldepth, gamma):
    """
    Menerapkan transformasi power-law (gamma correction) untuk mengubah kontras gambar.
    
    Args:
        img_input (PIL.Image): Objek gambar input yang akan diproses.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        gamma (float): Nilai gamma; <1 meningkatkan kecerahan, >1 meningkatkan kontras.
    
    Returns:
        PIL.Image: Objek gambar dengan koreksi gamma.
    """
    # Konversi gambar ke mode RGB jika bukan 24-bit untuk memudahkan manipulasi warna
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat gambar baru dengan ukuran yang sama untuk menyimpan hasil transformasi
    img_output = Image.new('RGB', img_input.size)
    pixels = img_output.load()  # Akses piksel gambar output untuk manipulasi
    
    # Iterasi setiap piksel untuk menerapkan transformasi power-law
    for i in range(img_output.size[0]):  # Loop melalui lebar gambar
        for j in range(img_output.size[1]):  # Loop melalui tinggi gambar
            r, g, b = img_input.getpixel((i, j))  # Ambil nilai RGB dari piksel input
            # Terapkan rumus power-law: 255 * (nilai/255)^gamma untuk setiap kanal warna
            r = int(255 * ((r / 255) ** gamma))  # Normalisasi ke 0-1, pangkat gamma, lalu kembali ke 0-255
            g = int(255 * ((g / 255) ** gamma))
            b = int(255 * ((b / 255) ** gamma))
            # Pastikan nilai RGB tetap dalam rentang 0-255
            pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna
    if coldepth == 1:
        img_output = img_output.convert("1")  # Konversi ke mode biner (1-bit)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Konversi ke mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Tetap di mode RGB (24-bit atau lebih)
    
    return img_output  # Kembalikan gambar hasil transformasi power-law

def ImgFlip(img_input, coldepth, flip_type):
    # Konversi gambar ke mode RGB jika bukan 24-bit
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat salinan gambar untuk diproses
    img_output = img_input.copy()
    
    # Terapkan flip berdasarkan flip_type
    if flip_type == "H":
        img_output = ImageOps.mirror(img_output)  # Flip horizontal
    elif flip_type == "V":
        img_output = ImageOps.flip(img_output)  # Flip vertikal
    elif flip_type == "HV":
        # Hanya flip vertikal dari gambar asli, tanpa horizontal
        img_output = ImageOps.flip(img_input.copy())  # Gunakan img_input asli untuk flip vertikal
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

def ImgZoom(img_input, coldepth, factor, zoom_type):
    """
    Melakukan zoom in atau zoom out pada gambar dengan faktor tertentu.
    
    Args:
        img_input (PIL.Image): Objek gambar input yang akan di-zoom.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        factor (float): Faktor zoom (misalnya, 2 untuk 2x, 0.5 untuk 1/2x).
        zoom_type (str): Jenis zoom ('in' untuk zoom in, 'out' untuk zoom out).
    
    Returns:
        PIL.Image: Objek gambar output yang telah di-zoom.
    """
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Dapatkan ukuran asli gambar
    original_width, original_height = img_input.size
    
    # Hitung ukuran baru berdasarkan faktor zoom
    if zoom_type == "in":
        new_width = int(original_width * factor)
        new_height = int(original_height * factor)
    elif zoom_type == "out":
        new_width = int(original_width / factor)
        new_height = int(original_height / factor)
    else:
        raise ValueError("zoom_type harus 'in' atau 'out'")
    
    # Pastikan ukuran baru tidak nol
    new_width = max(1, new_width)
    new_height = max(1, new_height)
    
    # Ubah ukuran gambar
    img_output = img_input.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Konversi kembali ke mode asli berdasarkan kedalaman warna
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output