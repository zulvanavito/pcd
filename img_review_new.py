# Impor modul mudul yang diperlukan
import PySimpleGUI as sg  # Modul untuk membuat antarmuka grafis (GUI)
import os.path  # Modul untuk manipulasi path file dan direktori
from PIL import Image, ImageOps  # Modul PIL untuk memproses gambar
from processing_list import ImgNegative, ImgRotate, ImgBrightness, ImgBlending, ImgLogarithmic, ImgPowerLaw  # Impor fungsi pengolahan gambar dari file processing_list.py

# --- Definisi Layout Antarmuka --- #

# Kolom Area No 1: Area untuk membuka folder dan memilih gambar
file_list_column = [
    [sg.Text("Open Image Folder:")],  # Label untuk menunjukkan area pemilihan folder gambar pertama
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"), sg.FolderBrowse()],  # Input teks dan tombol untuk memilih folder, dengan event aktif
    [sg.Text("Choose an image from list:")],  # Label untuk daftar gambar pertama
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList")],  # Listbox untuk menampilkan daftar file gambar, dengan event aktif
    [sg.Text("Second Image for Blending (optional):")],  # Label untuk area pemilihan folder gambar kedua (khusus blending)
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder2"), sg.FolderBrowse()],  # Input teks dan tombol untuk memilih folder kedua
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList2")],  # Listbox untuk daftar file gambar kedua
]

# Kolom Area No 2: Area untuk menampilkan gambar input pertama
image_viewer_column = [
    [sg.Text("Image Input:")],  # Label untuk area tampilan gambar input
    [sg.Text(size=(40, 1), key="FilepathImgInput")],  # Teks untuk menampilkan path file gambar yang dipilih
    [sg.Image(key="ImgInputViewer")],  # Komponen untuk menampilkan gambar input secara visual
]

# Kolom Area No 3: Area informasi gambar dan daftar tombol pengolahan
# Kolom Area No 3: Area informasi gambar dan daftar tombol pengolahan
list_processing = [
    [sg.Text("Image Information:")],  # Label untuk bagian informasi gambar
    [sg.Text(size=(20, 1), key="ImgSize")],  # Teks untuk menampilkan ukuran gambar
    [sg.Text(size=(20, 1), key="ImgColorDepth")],  # Teks untuk menampilkan kedalaman warna
    [sg.Text("List of Processing:")],  # Label untuk daftar tombol pengolahan gambar
    [sg.Button("Image Negative", size=(20, 1), key="ImgNegative")],  # Tombol negatif
    [sg.Button("Image Rotate", size=(20, 1), key="ImgRotate")],  # Tombol rotasi
    [sg.Button("Brightness", size=(20, 1), key="ImgBrightness")],  # Tombol kecerahan
    [sg.Button("Blending", size=(20, 1), key="ImgBlending")],  # Tombol blending
    [sg.Button("Logarithmic", size=(20, 1), key="ImgLogarithmic")],  # Tombol logaritmik
    [sg.Text("Logarithmic Constant (c):")],  # Label untuk slider konstanta c
    [sg.Slider(range=(1, 100), default_value=30, size=(20, 15), orientation='horizontal', key="LogC", enable_events=True)],  # Slider untuk c
    [sg.Button("Power Law", size=(20, 1), key="ImgPowerLaw")],  # Tombol power-law
]

# Kolom Area No 4: Area untuk menampilkan hasil pengolahan gambar
image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],  # Label untuk area tampilan hasil pengolahan
    [sg.Text(size=(40, 1), key="ImgProcessingType")],  # Teks untuk menampilkan jenis pengolahan yang dilakukan
    [sg.Image(key="ImgOutputViewer")],  # Komponen untuk menampilkan gambar hasil pengolahan
]

# Menggabungkan semua kolom menjadi layout utama dengan pemisah vertikal
layout = [
    [
        sg.Column(file_list_column, background_color='pink'),  # Kolom pertama: pemilihan gambar
        sg.VSeparator(),  # Pemisah vertikal antar kolom
        sg.Column(image_viewer_column, background_color='pink'),  # Kolom kedua: tampilan gambar input
        sg.VSeparator(),
        sg.Column(list_processing, background_color='pink'),  # Kolom ketiga: informasi dan tombol
        sg.VSeparator(),
        sg.Column(image_viewer_column2, background_color='pink'),  # Kolom keempat: tampilan hasil
    ]
]

# Membuat jendela GUI dengan judul "Mini Image Editor" menggunakan layout yang telah didefinisikan
window = sg.Window("Mini Image Editor", layout, background_color='pink')

# --- Definisi Variabel dan Data Pendukung ---

# Dictionary untuk memetakan mode gambar PIL ke kedalaman warna (dalam bit)
mode_to_coldepth = {
    "1": 1,      # Mode biner (1-bit, hitam-putih)
    "L": 8,      # Mode grayscale (8-bit)
    "P": 8,      # Mode palet (8-bit)
    "RGB": 24,   # Mode RGB (24-bit, 3x8)
    "RGBA": 32,  # Mode RGBA (32-bit, 4x8)
    "CMYK": 32,  # Mode CMYK (32-bit, 4x8)
    "YCbCr": 24, # Mode YCbCr (24-bit)
    "LAB": 24,   # Mode LAB (24-bit)
    "HSV": 24,   # Mode HSV (24-bit)
    "I": 32,     # Mode integer (32-bit)
    "F": 32      # Mode float (32-bit)
}

# Nama file sementara untuk menyimpan hasil pengolahan gambar
filename_out = "out.png"

# Variabel global untuk menyimpan data gambar dan informasi
img_input = None   # Menyimpan objek gambar pertama yang dipilih
img_input2 = None  # Menyimpan objek gambar kedua untuk blending (opsional)
coldepth = None    # Menyimpan kedalaman warna gambar pertama

# --- Event Loop: Logika Utama Program --- #

while True:
    # Membaca event dan nilai dari jendela GUI
    event, values = window.read()
    
    # Jika jendela ditutup atau tombol Exit diklik, keluar dari loop
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    # Event: Ketika folder untuk gambar pertama dipilih
    if event == "ImgFolder":
        folder = values["ImgFolder"]  # Ambil path folder dari input
        try:
            file_list = os.listdir(folder)  # Dapatkan daftar file di folder
        except Exception as e:
            print(f"Error membaca folder: {e}")  # Cetak pesan error jika gagal
            file_list = []  # Gunakan daftar kosong jika terjadi error
        
        # Filter hanya file gambar dengan ekstensi .png, atau .jpg
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg"))]
        window["ImgList"].update(fnames)  # Perbarui Listbox dengan daftar file gambar
    
    # Event: Ketika folder untuk gambar kedua (blending) dipilih
    if event == "ImgFolder2":
        folder = values["ImgFolder2"]  # Ambil path folder kedua
        try:
            file_list = os.listdir(folder)  # Dapatkan daftar file di folder
        except Exception as e:
            print(f"Error membaca folder: {e}")  # Cetak pesan error jika gagal
            file_list = []  # Gunakan daftar kosong jika terjadi error
        
        # Filter hanya file gambar dengan ekstensi .png, atau .jpg
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg"))]
        window["ImgList2"].update(fnames)  # Perbarui Listbox kedua dengan daftar file
    
    # Event: Ketika gambar pertama dipilih dari Listbox
    elif event == "ImgList" and values["ImgList"]:
        try:
            # Gabungkan path folder dan nama file untuk mendapatkan path lengkap
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(filename)  # Tampilkan path file di GUI
            window["ImgInputViewer"].update(filename=filename)  # Tampilkan gambar di viewer
            
            # Buka gambar menggunakan PIL dan simpan ke variabel global
            img_input = Image.open(filename)
            img_width, img_height = img_input.size  # Dapatkan dimensi gambar
            window["ImgSize"].update(f"Image Size: {img_width} x {img_height}")  # Tampilkan ukuran
            coldepth = mode_to_coldepth.get(img_input.mode, 24)  # Ambil kedalaman warna, default 24 jika tidak dikenal
            window["ImgColorDepth"].update(f"Color Depth: {coldepth}")  # Tampilkan kedalaman warna
            window["ImgProcessingType"].update("Original Image")  # Set jenis proses ke "Original"
            window["ImgOutputViewer"].update(filename=filename)  # Tampilkan gambar asli sebagai output awal
        
        except Exception as e:
            print(f"Error membuka gambar: {e}")  # Cetak pesan error jika gagal
    
    # Event: Ketika gambar kedua dipilih dari Listbox (untuk blending)
    elif event == "ImgList2" and values["ImgList2"]:
        try:
            # Gabungkan path folder dan nama file untuk gambar kedua
            filename2 = os.path.join(values["ImgFolder2"], values["ImgList2"][0])
            img_input2 = Image.open(filename2)  # Buka gambar kedua dan simpan ke variabel global
        except Exception as e:
            print(f"Error membuka gambar kedua: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses gambar menjadi negatif
    elif event == "ImgNegative" and img_input:
        try:
            window["ImgProcessingType"].update("Image Negative")  # Tampilkan jenis proses
            img_output = ImgNegative(img_input, coldepth)  # Panggil fungsi untuk membuat negatif
            img_output.save(filename_out)  # Simpan hasil ke file sementara
            window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil di viewer
        except Exception as e:
            print(f"Error memproses gambar negatif: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses rotasi gambar
    elif event == "ImgRotate" and img_input:
        try:
            window["ImgProcessingType"].update("Image Rotate")  # Tampilkan jenis proses
            img_output = ImgRotate(img_input, coldepth, 90, "C")  # Putar gambar 90 derajat searah jarum jam
            img_output.save(filename_out)  # Simpan hasil
            window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil
        except Exception as e:
            print(f"Error memutar gambar: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses penyesuaian kecerahan gambar
    elif event == "ImgBrightness" and img_input:
        try:
            # Tampilkan popup untuk meminta faktor kecerahan dari pengguna
            factor = sg.popup_get_text("Enter brightness factor (-255 to 255):", default_text="50")
            if factor:  # Jika pengguna memasukkan nilai
                window["ImgProcessingType"].update("Brightness")  # Tampilkan jenis proses
                img_output = ImgBrightness(img_input, coldepth, float(factor))  # Sesuaikan kecerahan
                img_output.save(filename_out)  # Simpan hasil
                window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil
        except Exception as e:
            print(f"Error menyesuaikan kecerahan: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses blending dua gambar
    elif event == "ImgBlending" and img_input:
        try:
            print(f"img_input2 status: {img_input2}")  # Cetak status gambar kedua untuk debugging
            if img_input2 is None:  # Periksa apakah gambar kedua telah dipilih
                sg.popup_error("Error", "Please select a second image for blending!")  # Tampilkan pesan error
                continue  # Keluar dari event ini jika gambar kedua belum ada
            # Tampilkan popup untuk meminta nilai alpha
            alpha = sg.popup_get_text("Enter alpha value (0.0 to 1.0):", default_text="0.5")
            if alpha:  # Jika pengguna memasukkan nilai
                window["ImgProcessingType"].update("Blending")  # Tampilkan jenis proses
                img_output = ImgBlending(img_input, img_input2, coldepth, float(alpha))  # Campur dua gambar
                img_output.save(filename_out)  # Simpan hasil
                window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil
        except Exception as e:
            print(f"Error blending gambar: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses transformasi logaritmik pada gambar
    elif event == "ImgLogarithmic" and img_input:
        try:
            c = values["LogC"]  # Ambil nilai konstanta c dari slider
            window["ImgProcessingType"].update("Logarithmic")  # Tampilkan jenis proses
            img_output = ImgLogarithmic(img_input, coldepth, float(c))  # Terapkan transformasi logaritmik
            img_output.save(filename_out)  # Simpan hasil
            window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil
        except Exception as e:
            print(f"Error transformasi logaritmik: {e}")  # Cetak pesan error jika gagal
            
            # Event: Ketika slider untuk konstanta c digeser
    elif event == "LogC" and img_input:
        try:
            c = values["LogC"]  # Ambil nilai konstanta c dari slider
            window["ImgProcessingType"].update("Logarithmic")  # Tampilkan jenis proses
            img_output = ImgLogarithmic(img_input, coldepth, float(c))  # Terapkan transformasi logaritmik
            img_output.save(filename_out)  # Simpan hasil
            window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil
        except Exception as e:
            print(f"Error transformasi logaritmik: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses transformasi power-law (gamma correction)
    elif event == "ImgPowerLaw" and img_input:
        try:
            # Tampilkan popup untuk meminta nilai gamma
            gamma = sg.popup_get_text("Enter gamma value:", default_text="1.5")
            if gamma:  # Jika pengguna memasukkan nilai
                window["ImgProcessingType"].update("Power Law")  # Tampilkan jenis proses
                img_output = ImgPowerLaw(img_input, coldepth, float(gamma))  # Terapkan transformasi power-law
                img_output.save(filename_out)  # Simpan hasil
                window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil
        except Exception as e:
            print(f"Error transformasi power-law: {e}")  # Cetak pesan error jika gagal

# Tutup jendela GUI setelah keluar dari loop
window.close()