import socket
import json
import cv2
from pyzbar.pyzbar import decode


def connect_to_server(qr_data, current_user_id, device_type):
    connection_data = json.loads(qr_data)
    ip_address = connection_data["ip"]
    port = connection_data["port"]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port))
    print(f"Conectado al servidor en {ip_address}:{port}")

    # Enviar el userId y tipo de dispositivo actual al servidor
    user_data = {"userId": current_user_id, "deviceType": device_type}
    client_socket.send(json.dumps(user_data).encode())
    response = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")
    client_socket.close()


def scan_qr_code():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        for barcode in decode(frame):
            qr_data = barcode.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return qr_data
        cv2.imshow("Scan QR Code", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return None


if __name__ == "__main__":
    qr_data = scan_qr_code()  # Escanea el QR y obtén los datos
    current_user_id = "current_user_id"
    device_type = "monitor"
    if qr_data:
        connect_to_server(qr_data, current_user_id, device_type)
    else:
        print("No se pudo escanear el código QR")