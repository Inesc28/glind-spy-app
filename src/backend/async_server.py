import asyncio

clients = {}  # Diccionario para almacenar clientes conectados

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Nueva conexión desde {addr}")
    userId = None

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode()
            print(f"Mensaje recibido de {addr}: {message}")

            if message.startswith("LINK_REQUEST:"):
                userId = message.split(":")[1]
                # Procesar la solicitud de vinculación
                # Por ejemplo, añadir el cliente al diccionario de clientes
                clients[userId] = writer
                response = f"Usuario {userId} vinculado correctamente."
                writer.write(response.encode())
                await writer.drain()
            else:
                # Manejar otros tipos de mensajes
                pass
    except Exception as e:
        print(f"Error con el cliente {addr}: {e}")
    finally:
        if userId and userId in clients:
            del clients[userId]
        writer.close()
        await writer.wait_closed()
        print(f"Conexión cerrada con {addr}")


async def start_async_server():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 65432)

    addr = server.sockets[0].getsockname()
    print(f"Servidor iniciado en {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start_async_server())
