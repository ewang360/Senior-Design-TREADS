import websockets
import time
import asyncio
import struct

async def handler(websocket):
    print("made connection!")
    count = 0
    while True:
        message = await websocket.recv()
        #print("a")
        print(len(message))
        floats = struct.unpack('4f', message)
        print("floats: ", floats)

async def main():
    async with websockets.serve(handler, "", PORT):
        await asyncio.Future()


PORT = 5777

asyncio.run(main())