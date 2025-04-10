# Impor modul yang diperlukan
import PySimpleGUI as sg
import os.path
from PIL import Image, ImageOps
from processing_list_new import *
import time

# --- Definisi Layout Antarmuka --- #

file_list_column = [
    [sg.Text("Open Image Folder:")],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"), sg.FolderBrowse()],
    [sg.Text("Choose an image from list:")],
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList")],
    [sg.Text("Second Image for Blending (optional):")],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder2"), sg.FolderBrowse()],
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList2")],
]

image_viewer_input1 = [
    [sg.Text("Image 1 Input (Primary):")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
    [sg.Text(size=(20, 1), key="ImgSize1")],
    [sg.Text(size=(20, 1), key="ImgColorDepth1")],
]

image_viewer_input2 = [
    [sg.Text("Second Image Input for Blending (Optional):")],
    [sg.Text(size=(40, 1), key="FilepathImgInput2")],
    [sg.Image(key="ImgInputViewer2")],
    [sg.Text(size=(20, 1), key="ImgSize2")],
    [sg.Text(size=(20, 1), key="ImgColorDepth2")],
]

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
    [sg.Button("Brightness", size=(37, 1), key="ImgBrightness")],
    [sg.Button("Blending", size=(37, 1), key="ImgBlending")],
    [sg.Text("Logarithmic Constant (c):")],
    [sg.Slider(range=(1, 100), default_value=30, orientation='h', size=(33, 15), key="LogC", enable_events=True)],
    [sg.Button("Logarithmic", size=(37, 1), key="ImgLogarithmic")],
    [sg.Button("Power Law", size=(37, 1), key="ImgPowerLaw")],
    [sg.Button("Reset All Operations", size=(37, 1), key="ResetAllOperations")],
]

image_viewer_ouput = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Text("Output File: out.png", size=(40, 1), key="FilepathImgOutput")],
    # Bungkus ImgOutputViewer dalam Column dengan scroll
    [sg.Column(
        [[sg.Image(key="ImgOutputViewer")]],  # Gambar output
        size=(300, 300),  # Ukuran area tampilan
        scrollable=True,  # Aktifkan scroll
        vertical_scroll_only=False,  # Izinkan scroll vertikal dan horizontal
        key="OutputColumn",  # Beri key untuk referensi
        expand_x=True,
        expand_y=True,
    )],
    [sg.Text(size=(20, 1), key="ImgSizeOutput")],
    [sg.Text(size=(20, 1), key="ImgColorDepthOutput")],
    [sg.Text(size=(20, 1), key="ImgModeOutput")],
    [sg.Text(size=(30, 1), key="ProcessingTimeOutput")],
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_input1),
        sg.VSeparator(),
        sg.Column(image_viewer_input2),
        sg.VSeparator(),
        sg.Column(list_processing),
        sg.VSeparator(),
        sg.Column(image_viewer_ouput),
    ]
]

window = sg.Window("Mini Image Editor", layout)

# --- Definisi Variabel dan Data Pendukung ---

mode_to_coldepth = {
    "1": 1,
    "L": 8,
    "P": 8,
    "RGB": 24,
    "RGBA": 32,
    "CMYK": 32,
    "YCbCr": 24,
    "LAB": 24,
    "HSV": 24,
    "I": 32,
    "F": 32
}

filename_out = "out.png"

img_input = None
img_input2 = None
coldepth = None

# --- Event Loop: Logika Utama Program --- #

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    # Event: Ketika folder untuk gambar pertama dipilih
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        print(f"Folder dipilih: {folder}")
        if not folder:
            sg.popup_error("Error", "Silakan pilih folder yang valid!")
            continue
        try:
            file_list = os.listdir(folder)
            print(f"File dalam folder: {file_list}")
        except Exception as e:
            print(f"Error membaca folder: {e}")
            sg.popup_error("Error", f"Error membaca folder: {e}")
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))]
        print(f"File gambar yang ditemukan: {fnames}")
        if not fnames:
            sg.popup("Info", "Tidak ada file gambar (.png, .jpg, .jpeg, .bmp, .gif) di folder ini!")
        window["ImgList"].update(fnames)
        window.refresh()
    
    # Event: Ketika folder untuk gambar kedua (blending) dipilih
    if event == "ImgFolder2":
        folder = values["ImgFolder2"]
        print(f"Folder kedua dipilih: {folder}")
        if not folder:
            sg.popup_error("Error", "Silakan pilih folder yang valid untuk gambar kedua!")
            continue
        try:
            file_list = os.listdir(folder)
            print(f"File dalam folder kedua: {file_list}")
        except Exception as e:
            print(f"Error membaca folder: {e}")
            sg.popup_error("Error", f"Error membaca folder: {e}")
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))]
        print(f"File gambar yang ditemukan untuk folder kedua: {fnames}")
        if not fnames:
            sg.popup("Info", "Tidak ada file gambar (.png, .jpg, .jpeg, .bmp, .gif) di folder ini!")
        window["ImgList2"].update(fnames)
        window.refresh()
    
    # Event: Ketika gambar pertama dipilih dari Listbox
    elif event == "ImgList" and values["ImgList"]:
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(filename)
            window["ImgInputViewer"].update(filename=filename)
        
            img_input = Image.open(filename)
            img_width, img_height = img_input.size
            window["ImgSize1"].update(f"Image Size: {img_width} x {img_height}")
            coldepth = mode_to_coldepth.get(img_input.mode, 24)
            window["ImgColorDepth1"].update(f"Color Depth: {coldepth}")
            window["ImgProcessingType"].update("Original Image")
            window["ImgOutputViewer"].update(filename=filename)
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, img_width), max(300, img_height)))
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {img_width} x {img_height}")
            window["ImgColorDepthOutput"].update(f"Color Depth: {coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_input.mode}")
            window["ProcessingTimeOutput"].update("Processing Time: N/A")
        except Exception as e:
            print(f"Error membuka gambar: {e}")
            sg.popup_error("Error", f"Error membuka gambar: {e}")
    
    # Event: Ketika gambar kedua dipilih dari Listbox (untuk blending)
    elif event == "ImgList2" and values["ImgList2"]:
        try:
            filename2 = os.path.join(values["ImgFolder2"], values["ImgList2"][0])
            window["FilepathImgInput2"].update(filename2)
            window["ImgInputViewer2"].update(filename=filename2)
        
            img_input2 = Image.open(filename2)
            img_width2, img_height2 = img_input2.size
            window["ImgSize2"].update(f"Image Size: {img_width2} x {img_height2}")
            coldepth2 = mode_to_coldepth.get(img_input2.mode, 24)
            window["ImgColorDepth2"].update(f"Color Depth: {coldepth2}")
        except Exception as e:
            print(f"Error membuka gambar kedua: {e}")
            sg.popup_error("Error", f"Error membuka gambar kedua: {e}")
    
    # Event: Proses zoom in
    elif event == "ZoomIn" and img_input:
        try:
            factor = int(values["ZoomInFactor"].replace("x", ""))
            window["ImgProcessingType"].update(f"Zoom In {factor}x")
            start_time = time.time()
            img_output = ImgZoom(img_input, coldepth, factor, "in")
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1, biarkan tetap menunjukkan ukuran gambar input
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error zoom in: {e}")
            sg.popup_error("Error", f"Error zoom in: {e}")
    
    # Event: Proses zoom out
    elif event == "ZoomOut" and img_input:
        try:
            factor = int(values["ZoomOutFactor"].replace("x", ""))
            window["ImgProcessingType"].update(f"Zoom Out {factor}x")
            start_time = time.time()
            img_output = ImgZoom(img_input, coldepth, factor, "out")
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error zoom out: {e}")
            sg.popup_error("Error", f"Error zoom out: {e}")
    
    # Event: Proses gambar menjadi negatif
    elif event == "ImgNegative" and img_input:
        try:
            window["ImgProcessingType"].update("Image Negative")
            start_time = time.time()
            img_output = ImgNegative(img_input, coldepth)
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error memproses gambar negatif: {e}")
            sg.popup_error("Error", f"Error memproses gambar negatif: {e}")
    
    # Event: Proses rotasi gambar untuk setiap sudut
    elif event in ("Rotate-90", "Rotate90", "Rotate180") and img_input:
        try:
            degrees = int(event.replace("Rotate", ""))
            direction_text = "Counterclockwise" if degrees < 0 else "Clockwise" if degrees == 90 else ""
            window["ImgProcessingType"].update(f"Image Rotate {abs(degrees)}° {direction_text}")
            start_time = time.time()
            img_output = ImgRotate(img_input, coldepth, degrees)
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error memutar gambar: {e}")
            sg.popup_error("Error", f"Error memutar gambar: {e}")
    
    # Event: Proses flip gambar
    elif event in ("FlipH", "FlipV", "FlipHV") and img_input:
        try:
            flip_type = event.replace("Flip", "")
            window["ImgProcessingType"].update(f"Flip {flip_type}")
            start_time = time.time()
            img_output = ImgFlip(img_input, coldepth, flip_type)
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error membalik gambar: {e}")
            sg.popup_error("Error", f"Error membalik gambar: {e}")
    
    # Event: Proses penyesuaian kecerahan gambar
    elif event == "ImgBrightness" and img_input:
        try:
            factor = sg.popup_get_text("Enter brightness factor (-255 to 255):", default_text="50")
            if factor:
                window["ImgProcessingType"].update("Brightness")
                start_time = time.time()
                img_output = ImgBrightness(img_input, coldepth, float(factor))
                end_time = time.time()
                processing_time = end_time - start_time
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(filename=filename_out)
                new_width, new_height = img_output.size
                # Perbarui ukuran Column berdasarkan ukuran gambar
                window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
                # Jangan perbarui ImgSize1
                window["FilepathImgOutput"].update("Output File: out.png")
                window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
                new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
                window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
                window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
                window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error menyesuaikan kecerahan: {e}")
            sg.popup_error("Error", f"Error menyesuaikan kecerahan: {e}")
    
    # Event: Proses blending dua gambar
    elif event == "ImgBlending" and img_input:
        try:
            if img_input2 is None:
                sg.popup_error("Error", "Please select a second image for blending!")
                continue
            alpha = sg.popup_get_text("Enter alpha value (0.0 to 1.0):", default_text="0.5")
            if alpha:
                window["ImgProcessingType"].update("Blending")
                start_time = time.time()
                img_output = ImgBlending(img_input, img_input2, coldepth, float(alpha))
                end_time = time.time()
                processing_time = end_time - start_time
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(filename=filename_out)
                new_width, new_height = img_output.size
                # Perbarui ukuran Column berdasarkan ukuran gambar
                window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
                # Jangan perbarui ImgSize1
                window["FilepathImgOutput"].update("Output File: out.png")
                window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
                new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
                window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
                window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
                window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error blending gambar: {e}")
            sg.popup_error("Error", f"Error blending gambar: {e}")
    
    # Event: Proses transformasi logaritmik pada gambar
    elif event == "ImgLogarithmic" and img_input:
        try:
            c = values["LogC"]
            if c is None:
                c = 30
            window["ImgProcessingType"].update("Logarithmic")
            start_time = time.time()
            img_output = ImgLogarithmic(img_input, coldepth, float(c))
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error transformasi logaritmik: {e}")
            sg.popup_error("Error", f"Error transformasi logaritmik: {e}")
    
    # Event: Ketika slider untuk konstanta c digeser
    elif event == "LogC" and img_input:
        try:
            c = values["LogC"]
            window["ImgProcessingType"].update("Logarithmic")
            start_time = time.time()
            img_output = ImgLogarithmic(img_input, coldepth, float(c))
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            new_width, new_height = img_output.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
            # Jangan perbarui ImgSize1
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error transformasi logaritmik: {e}")
            sg.popup_error("Error", f"Error transformasi logaritmik: {e}")
    
    # Event: Proses transformasi power-law (gamma correction)
    elif event == "ImgPowerLaw" and img_input:
        try:
            gamma = sg.popup_get_text("Enter gamma value:", default_text="1.5")
            if gamma:
                window["ImgProcessingType"].update("Power Law")
                start_time = time.time()
                img_output = ImgPowerLaw(img_input, coldepth, float(gamma))
                end_time = time.time()
                processing_time = end_time - start_time
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(filename=filename_out)
                new_width, new_height = img_output.size
                # Perbarui ukuran Column berdasarkan ukuran gambar
                window["OutputColumn"].set_size((max(300, new_width), max(300, new_height)))
                # Jangan perbarui ImgSize1
                window["FilepathImgOutput"].update("Output File: out.png")
                window["ImgSizeOutput"].update(f"Image Size: {new_width} x {new_height}")
                new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
                window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
                window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
                window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
        except Exception as e:
            print(f"Error transformasi power-law: {e}")
            sg.popup_error("Error", f"Error transformasi power-law: {e}")
    
    # Event: Reset semua operasi
    elif event == "ResetAllOperations" and img_input:
        try:
            start_time = time.time()
            img_output = img_input.copy()
            end_time = time.time()
            processing_time = end_time - start_time
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
            original_width, original_height = img_input.size
            # Perbarui ukuran Column berdasarkan ukuran gambar
            window["OutputColumn"].set_size((max(300, original_width), max(300, original_height)))
            # Jangan perbarui ImgSize1, sudah diatur saat gambar dipilih
            window["FilepathImgOutput"].update("Output File: out.png")
            window["ImgSizeOutput"].update(f"Image Size: {original_width} x {original_height}")
            new_coldepth = mode_to_coldepth.get(img_output.mode, 24)
            window["ImgColorDepthOutput"].update(f"Color Depth: {new_coldepth}")
            window["ImgModeOutput"].update(f"Image Mode: {img_output.mode}")
            window["ProcessingTimeOutput"].update(f"Processing Time: {processing_time:.3f} seconds")
            img_input2 = None
            window["ImgInputViewer2"].update(filename=None)
            window["ImgSize2"].update("Image Size: ")
            window["FilepathImgInput2"].update("")
            window["ImgColorDepth2"].update("Color Depth: ")
            window["ImgProcessingType"].update("Original Image")
            window["LogC"].update(30)  # Kembalikan slider ke nilai default (30)
        except Exception as e:
            print(f"Error reset semua operasi: {e}")
            sg.popup_error("Error", f"Error reset semua operasi: {e}")

window.close()