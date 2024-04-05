import asyncio
import websockets

async def hello():
    uri = "ws://172.24.208.1:8765"
    async with websockets.connect(uri) as websocket:
        ip = await websocket.recv()
        print(f"<<<{ip}")

if __name__ == "__main__":
    asyncio.run(hello())