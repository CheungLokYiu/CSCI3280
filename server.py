import asyncio
import websockets
import socket

async def hello(websocket):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Connect the socket to a public DNS server's IP (Google's in this case)
    s.connect(("8.8.8.8", 80))

    # Get the socket's own IP address
    ip = s.getsockname()[0]

    # Close the dummy socket
    s.close()

    await websocket.send(ip)
    print(f">>>{ip}")

async def main():
    async with websockets.serve(hello, "172.24.208.1", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())