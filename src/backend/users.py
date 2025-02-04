import string
import random
import qrcode

users = {
    "VE0001ABC": {
        "email": "sant@gmail.com",
        "user": "sant04",
        "password": "12345",
        "linked_devices": ["VE0002DEF"],
    },
    "VE0002DEF": {
        "email": "acness@hotmail.com",
        "user": "acness08",
        "password": "67890",
        "linked_devices": ["VE0001ABC", "VE0003GHI"],
    },
    "VE0003GHI": {
        "email": "sidness@example.com",
        "user": "sidness26",
        "password": "98765",
        "linked_devices": ["VE0001ABC"],
    },
}


def generate_user_id(pais="VE"):
    nums = "".join((random.choices(string.ascii_uppercase, k=4)))
    ch = "".join((random.choices(string.digits, k=4)))
    return f"{pais}{nums}{ch}"


def register_new_user(email, user, password):
    asignedId = generate_user_id()
    if asignedId in users:
        register_new_user(email, user, password)
    users[asignedId] = {"email": email, "user": user, "password": password}
    print(users)


def validate_user(user, password):
    for userId, user_data in users.items():
        if user == user_data["user"]:
            if password == user_data["password"]:
                print("Inicio de sesión exitoso")
                return userId  # Devuelves el ID del usuario
            else:
                print("La contraseña es incorrecta.")
                return None
    print("El usuario ingresado no existe.")
    return None


def generate_qr(userId):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(userId)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{userId}.png")


def get_user_data(user_id):
    return {"id": user_id, "user": users[user_id]["user"]} if user_id in users else None

