import PySimpleGUI as sg
import os.path
from PIL import Image, ImageOps
from processing_list import ImgNegative, ImgRotate  # Impor fungsi dari processing_list

# Kolom Area No 1: Area open folder and select image
file_list_column = [
    [sg.Text("Open Image Folder:")],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"), sg.FolderBrowse()],
    [sg.Text("Choose an image from list:")],
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList")],
]

# Kolom Area No 2: Area viewer image input
image_viewer_column = [
    [sg.Text("Image Input:")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

# Kolom Area No 3: Area Image info dan Tombol list of processing
list_processing = [
    [sg.Text("Image Information:")],
    [sg.Text(size=(20, 1), key="ImgSize")],
    [sg.Text(size=(20, 1), key="ImgColorDepth")],
    [sg.Text("List of Processing:")],
    [sg.Button("Image Negative", size=(20, 1), key="ImgNegative")],
    [sg.Button("Image Rotate", size=(20, 1), key="ImgRotate")],
]

# Kolom Area No 4: Area viewer image output
image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]

# Gabung Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
        sg.VSeparator(),
        sg.Column(list_processing),
        sg.VSeparator(),
        sg.Column(image_viewer_column2),
    ]
]

# Membuat window
window = sg.Window("Mini Image Editor", layout)

# Dictionary untuk mapping mode gambar ke color depth
mode_to_coldepth = {
    "1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32,
    "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32
}

# Nama file temporary untuk output processing
filename_out = "out.png"

# Variabel untuk menyimpan gambar input (digunakan di event processing)
img_input = None
coldepth = None

# Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    # Event untuk mengisi daftar file saat folder dipilih
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            file_list = os.listdir(folder)
        except Exception as e:
            print(f"Error membaca folder: {e}")
            file_list = []
        
        fnames = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", ".jpg"))
        ]
        window["ImgList"].update(fnames)
    
    # Event untuk menampilkan gambar yang dipilih dari listbox
    elif event == "ImgList" and values["ImgList"]:
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(filename)
            window["ImgInputViewer"].update(filename=filename)
            
            # Buka gambar dengan Pillow
            img_input = Image.open(filename)
            
            # Update ukuran gambar
            img_width, img_height = img_input.size
            window["ImgSize"].update(f"Image Size: {img_width} x {img_height}")
            
            # Update color depth
            coldepth = mode_to_coldepth.get(img_input.mode, 24)  # Default ke 24 jika tidak dikenali
            window["ImgColorDepth"].update(f"Color Depth: {coldepth}")
            
            # Tampilkan gambar di output viewer sebagai default
            window["ImgProcessingType"].update("Original Image")
            window["ImgOutputViewer"].update(filename=filename)
        
        except Exception as e:
            print(f"Error membuka gambar: {e}")
    
    # Event untuk memproses gambar menjadi negatif
    elif event == "ImgNegative" and img_input:
        try:
            window["ImgProcessingType"].update("Image Negative")
            img_output = ImgNegative(img_input, coldepth)
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error memproses gambar negatif: {e}")
    
    # Event untuk memutar gambar
    elif event == "ImgRotate" and img_input:
        try:
            window["ImgProcessingType"].update("Image Rotate")
            img_output = ImgRotate(img_input, coldepth, 90, "C")  # Rotasi 90° clockwise
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error memutar gambar: {e}")

window.close()