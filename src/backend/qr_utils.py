# src/backend/qr_utils.py

import qrcode
from PIL import Image
from pyzbar.pyzbar import decode


def generate_qr(data, filename):
    """
    Genera un código QR a partir de los datos proporcionados y lo guarda como una imagen PNG.

    :param data: Datos que se codificarán en el QR.
    :param filename: Nombre del archivo PNG que se generará (sin extensión).
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{filename}.png")
    print(f"Código QR generado y guardado como {filename}.png")


def scan_qr(image_path):
    """
    Lee un código QR de una imagen y devuelve los datos contenidos.

    :param image_path: Ruta al archivo de imagen que contiene el código QR.
    :return: Datos decodificados del código QR o None si no se pudo leer.
    """
    try:
        img = Image.open(image_path)
        decoded = decode(img)
        if decoded:
            data = decoded[0].data.decode("utf-8")
            return data
        else:
            print("No se pudo leer el código QR.")
            return None
    except FileNotFoundError:
        print(f"No se encontró el archivo {image_path}.")
        return None
    except Exception as e:
        print(f"Error al escanear el código QR: {e}")
        return None
