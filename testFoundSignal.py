import websockets
import time
import smbus2
import asyncio
import struct

async def handler(websocket):
    print("made connection!")
    count = 0
    while True:
        if (count%10==0)
            await websocket.send("found")
        count++
        
async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()

PORT = 5779   

asyncio.run(main())
