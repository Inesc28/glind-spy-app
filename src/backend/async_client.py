import asyncio

async def connect_to_server(host, port, userId):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        message = f"LINK_REQUEST:{userId}"
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(1024)
        print(f"Respuesta del servidor: {data.decode()}")

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")

