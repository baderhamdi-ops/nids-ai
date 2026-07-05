import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://localhost:8000/api/ws/alerts") as ws:
        print("Connected. Waiting for messages...")
        while True:
            msg = await ws.recv()
            print("Received:", msg)

asyncio.run(listen())
