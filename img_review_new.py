# Impor modul mudul yang diperlukan
import PySimpleGUI as sg  # Modul untuk membuat antarmuka grafis (GUI)
import os.path  # Modul untuk manipulasi path file dan direktori
from PIL import Image, ImageOps  # Modul PIL untuk memproses gambar
from processing_list_new import * # Impor fungsi pengolahan gambar dari file processing_list.py

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
    [sg.Text("Image 1 Input (Primary):")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
    [sg.Text(size=(20, 1), key="ImgSize1")],  # Informasi ukuran untuk gambar pertama
    [sg.Text(size=(20, 1), key="ImgColorDepth1")],  # Informasi kedalaman warna untuk gambar pertama
]

# Kolom Area No 2b: Area untuk menampilkan gambar input kedua
image_viewer_column2_input = [
    [sg.Text("Second Image Input for Blending (Optional):")],
    [sg.Text(size=(40, 1), key="FilepathImgInput2")],
    [sg.Image(key="ImgInputViewer2")],
    [sg.Text(size=(20, 1), key="ImgSize2")],  # Informasi ukuran untuk gambar kedua
    [sg.Text(size=(20, 1), key="ImgColorDepth2")],  # Informasi kedalaman warna untuk gambar kedua
]

# Kolom Area No 3: Area daftar tombol pengolahan
list_processing = [
    [sg.Text("List of Processing:")],
    [sg.Button("Image Negative", size=(37, 1), key="ImgNegative")],
    [sg.Text("Rotate (degrees):")],
    [sg.Button("-90° (CCW)", size=(10, 1), key="Rotate-90"),
     sg.Button("90° (CW)", size=(10, 1), key="Rotate90"),
     sg.Button("180°", size=(10, 1), key="Rotate180")],
    [sg.Text("Flip Image:")],
    [sg.Button("Horizontal", size=(10, 1), key="FlipH"),
     sg.Button("Vertical", size=(10, 1), key="FlipV"),
     sg.Button("Both", size=(10, 1), key="FlipHV")],
    [sg.Text("Zoom:")],
    [sg.Combo(["2x", "3x", "4x"], default_value="2x", size=(22, 1), key="ZoomInFactor", enable_events=True),
     sg.Button("Zoom In", size=(10, 1), key="ZoomIn")],
    [sg.Combo(["2x", "3x", "4x"], default_value="2x", size=(22, 1), key="ZoomOutFactor", enable_events=True),
     sg.Button("Zoom Out", size=(10, 1), key="ZoomOut")],
    [sg.Button("Reset Zoom", size=(37, 1), key="ResetZoom")],
    [sg.Button("Brightness", size=(37, 1), key="ImgBrightness")],
    [sg.Button("Blending", size=(37, 1), key="ImgBlending")],
    [sg.Text("Logarithmic Constant (c):")],
    [sg.Slider(range=(1, 100), default_value=30, orientation='h', size=(33, 15), key="LogC", enable_events=True)],
    [sg.Button("Logarithmic", size=(37, 1), key="ImgLogarithmic")],
    [sg.Button("Power Law", size=(37, 1), key="ImgPowerLaw")],
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
        sg.Column(file_list_column),  # Kolom pertama: pemilihan gambar
        sg.VSeparator(),  # Pemisah vertikal antar kolom
        sg.Column(image_viewer_column),  # Kolom kedua: tampilan gambar input pertama
        sg.VSeparator(),
        sg.Column(image_viewer_column2_input),  # Kolom baru: tampilan gambar input kedua
        sg.VSeparator(),
        sg.Column(list_processing),  # Kolom ketiga: informasi dan tombol
        sg.VSeparator(),
        sg.Column(image_viewer_column2),  # Kolom keempat: tampilan hasil
    ]
]

# Membuat jendela GUI dengan judul "Mini Image Editor" menggunakan layout yang telah didefinisikan
window = sg.Window("Mini Image Editor", layout)

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
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(filename)
            window["ImgInputViewer"].update(filename=filename)
        
            img_input = Image.open(filename)
            img_width, img_height = img_input.size
            window["ImgSize1"].update(f"Image Size: {img_width} x {img_height}")  # Perbarui ukuran gambar 1
            coldepth = mode_to_coldepth.get(img_input.mode, 24)
            window["ImgColorDepth1"].update(f"Color Depth: {coldepth}")  # Perbarui kedalaman warna gambar 1
            window["ImgProcessingType"].update("Original Image")
            window["ImgOutputViewer"].update(filename=filename)
        except Exception as e:
            print(f"Error membuka gambar: {e}")
    
    # Event: Ketika gambar kedua dipilih dari Listbox (untuk blending)
    elif event == "ImgList2" and values["ImgList2"]:
        try:
            filename2 = os.path.join(values["ImgFolder2"], values["ImgList2"][0])
            window["FilepathImgInput2"].update(filename2)
            window["ImgInputViewer2"].update(filename=filename2)
        
            img_input2 = Image.open(filename2)
            img_width2, img_height2 = img_input2.size
            window["ImgSize2"].update(f"Image Size: {img_width2} x {img_height2}")  # Perbarui ukuran gambar 2
            coldepth2 = mode_to_coldepth.get(img_input2.mode, 24)
            window["ImgColorDepth2"].update(f"Color Depth: {coldepth2}")  # Perbarui kedalaman warna gambar 2
        except Exception as e:
            print(f"Error membuka gambar kedua: {e}")
    
    # Event: Proses gambar menjadi negatif
    elif event == "ImgNegative" and img_input:
        try:
            window["ImgProcessingType"].update("Image Negative")  # Tampilkan jenis proses
            img_output = ImgNegative(img_input, coldepth)  # Panggil fungsi untuk membuat negatif
            img_output.save(filename_out)  # Simpan hasil ke file sementara
            window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil di viewer
        except Exception as e:
            print(f"Error memproses gambar negatif: {e}")  # Cetak pesan error jika gagal
    
    # Event: Proses rotasi gambar untuk setiap sudut
    elif event in ("Rotate-90", "Rotate90", "Rotate180") and img_input:
        try:
            # Ambil sudut dari nama event (hapus "Rotate" dari string event)
            degrees = int(event.replace("Rotate", ""))
            # Tentukan arah rotasi untuk teks
            direction_text = "Counterclockwise" if degrees < 0 else "Clockwise" if degrees == 90 else ""
            window["ImgProcessingType"].update(f"Image Rotate {abs(degrees)}° {direction_text}")
            img_output = ImgRotate(img_input, coldepth, degrees)  # Gunakan sudut langsung
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error memutar gambar: {e}")
    
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
            c = values["LogC"]  # Ambil nilai dari slider
            if c is None:  # Jika slider belum diatur
                c = 30  # Gunakan nilai default
            window["ImgProcessingType"].update("Logarithmic")
            img_output = ImgLogarithmic(img_input, coldepth, float(c))
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error transformasi logaritmik: {e}")

    # Event: Ketika slider untuk konstanta c digeser (opsional untuk pembaruan real-time)
    elif event == "LogC" and img_input:
        try:
            c = values["LogC"]  # Ambil nilai dari slider
            window["ImgProcessingType"].update("Logarithmic")
            img_output = ImgLogarithmic(img_input, coldepth, float(c))
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error transformasi logaritmik: {e}")
    
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

    # Event: Proses flip gambar
    elif event in ("FlipH", "FlipV", "FlipHV") and img_input:
        try:
            flip_type = event.replace("Flip", "")  # Ambil jenis flip dari nama event (H, V, atau HV)
            window["ImgProcessingType"].update(f"Flip {flip_type}")
            img_output = ImgFlip(img_input, coldepth, flip_type)  # Panggil fungsi flip
            img_output.save(filename_out)  # Simpan hasil ke file sementara
            window["ImgOutputViewer"].update(filename=filename_out)  # Tampilkan hasil di viewer
        except Exception as e:
            print(f"Error membalik gambar: {e}")
            
    # Event: Proses zoom in
    elif event == "ZoomIn" and img_input:
        try:
            factor = int(values["ZoomInFactor"].replace("x", ""))  # Ambil faktor dari dropdown (hapus "x")
            window["ImgProcessingType"].update(f"Zoom In {factor}x")
            img_output = ImgZoom(img_input, coldepth, factor, "in")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            # Perbarui informasi ukuran gambar di viewer
            new_width, new_height = img_output.size
            window["ImgSize1"].update(f"Image Size: {new_width} x {new_height}")
        except Exception as e:
            print(f"Error zoom in: {e}")

# Event: Proses zoom out
    elif event == "ZoomOut" and img_input:
        try:
            factor = int(values["ZoomOutFactor"].replace("x", ""))  # Ambil faktor dari dropdown (hapus "x")
            window["ImgProcessingType"].update(f"Zoom Out {factor}x")
            img_output = ImgZoom(img_input, coldepth, factor, "out")
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            # Perbarui informasi ukuran gambar di viewer
            new_width, new_height = img_output.size
            window["ImgSize1"].update(f"Image Size: {new_width} x {new_height}")
        except Exception as e:
            print(f"Error zoom out: {e}")

    # Event: Reset zoom
    elif event == "ResetZoom" and img_input:
        try:
            window["ImgProcessingType"].update("Reset Zoom")
            img_output = img_input.copy()  # Kembali ke gambar asli
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            # Perbarui informasi ukuran gambar di viewer
            original_width, original_height = img_input.size
            window["ImgSize1"].update(f"Image Size: {original_width} x {original_height}")
        except Exception as e:
            print(f"Error reset zoom: {e}")
            
# Tutup jendela GUI setelah keluar dari loop
window.close()