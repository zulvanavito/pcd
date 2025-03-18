#Kode Default
elif event == "ImgBlending" and img_input and img_input2:
        try:
            alpha = sg.popup_get_text("Enter alpha value (0.0 to 1.0):", default_text="0.5")
            if alpha:
                window["ImgProcessingType"].update("Blending")
                img_output = ImgBlending(img_input, img_input2, coldepth, float(alpha))
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error blending gambar: {e}")

#Kode 1 Custom Pop Up
elif event == "ImgBlending" and img_input:
        try:
            print(f"img_input2 status: {img_input2}")  # Debug
            if img_input2 is None:
                sg.popup_error("Error", "Please select a second image for blending!")
                continue  # Keluar dari event ini
            alpha = sg.popup_get_text("Enter alpha value (0.0 to 1.0):", default_text="0.5")
            if alpha:
                window["ImgProcessingType"].update("Blending")
                img_output = ImgBlending(img_input, img_input2, coldepth, float(alpha))
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(filename=filename_out)
        except Exception as e:
            print(f"Error blending gambar: {e}")