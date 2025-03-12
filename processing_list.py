from PIL import Image, ImageOps

def ImgNegative(img_input, coldepth):
    """
    Mengubah gambar menjadi negatif berdasarkan color depth.
    
    Args:
        img_input (PIL.Image): Gambar input yang akan diproses.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
    
    Returns:
        PIL.Image: Gambar output dalam bentuk negatif.
    """
    # Jika coldepth bukan 24 (RGB), konversi ke RGB terlebih dahulu
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat gambar baru dengan mode RGB dan ukuran yang sama
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()  # Akses piksel untuk manipulasi
    
    # Proses setiap piksel untuk membuat negatif
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i, j] = (255 - r, 255 - g, 255 - b)
    
    # Konversi kembali ke mode asli berdasarkan coldepth
    if coldepth == 1:
        img_output = img_output.convert("1")  # Mode biner (1-bit)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Mode RGB (24-bit atau lebih)
    
    return img_output

def ImgRotate(img_input, coldepth, deg, direction):
    """
    Memutar gambar berdasarkan derajat dan arah tertentu.
    
    Args:
        img_input (PIL.Image): Gambar input yang akan diproses.
        coldepth (int): Kedalaman warna gambar (1, 8, atau 24/32).
        deg (int): Derajat rotasi (tidak digunakan langsung di solusi 2).
        direction (str): Arah rotasi ('C' untuk clockwise, lainnya untuk counterclockwise).
    
    Returns:
        PIL.Image: Gambar output yang telah diputar.
    """
    # Jika coldepth bukan 24 (RGB), konversi ke RGB terlebih dahulu
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Buat gambar baru dengan ukuran terbalik (lebar menjadi tinggi, tinggi menjadi lebar)
    img_output = Image.new('RGB', (img_input.size[1], img_input.size[0]))
    pixels = img_output.load()  # Akses piksel untuk manipulasi
    
    # Proses setiap piksel untuk rotasi
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if direction == "C":  # Clockwise (searah jarum jam)
                r, g, b = img_input.getpixel((j, img_output.size[0] - i - 1))
            else:  # Counterclockwise (berlawanan arah jarum jam)
                r, g, b = img_input.getpixel((img_input.size[1] - j - 1, i))
            pixels[i, j] = (r, g, b)
    
    # Konversi kembali ke mode asli berdasarkan coldepth
    if coldepth == 1:
        img_output = img_output.convert("1")  # Mode biner (1-bit)
    elif coldepth == 8:
        img_output = img_output.convert("L")  # Mode grayscale (8-bit)
    else:
        img_output = img_output.convert("RGB")  # Mode RGB (24-bit atau lebih)
    
    return img_output

# Catatan: Solusi alternatif untuk rotasi menggunakan Image.rotate()
# def ImgRotate(img_input, coldepth, deg, direction):
#     img_output = img_input.rotate(deg if direction == "C" else -deg)
#     return img_output