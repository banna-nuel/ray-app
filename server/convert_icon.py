
from PIL import Image
import os

def convert_to_ico():
    input_path = r"C:\unipaz\tic\ray-app\ray-app-web\public\logo-ray.png"
    output_path = r"C:\unipaz\tic\ray-app\server\logo.ico"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} no existe")
        return

    img = Image.open(input_path)
    # Redimensionar para mejor compatibilidad con iconos de Windows
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(output_path, format='ICO', sizes=icon_sizes)
    print(f"✓ Icono creado en: {output_path}")

if __name__ == "__main__":
    convert_to_ico()
